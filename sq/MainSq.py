import json
import logging
import os.path
logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(name)s:%(levelname)s: %(message)s",
)
logger = logging.getLogger("DoSq")
'''
1.根据股票代码和日期 加载文件中对应的行情和逐笔数据(文件中的数据为全量，需过滤出9:30 - 11:30, 13:00 - 15:00这两个时间段的数据)。
2.对过滤出的行情和逐笔做匹配(一个tick对应的哪些逐笔成交数据,行情和逐笔均有时间字段) ，然后将这些数据返回。
3.tick 匹配规则 >上一个tick的时间 <=当前tick的时间
'''


class MatchingWorker(object):
    """
    执行匹配的单元模块
    建议由MatchingWorkBuilder.create_worker来创建
    创建后执行run开始匹配返回List<MatchingBean>
    """
    def __init__(self, pathQuotation, pathTransaction, stockCode):
        self.matchingList = []
        self.pathQuotationFile = os.path.join(pathQuotation, stockCode + ".txt")
        self.pathTransactionFile = os.path.join(pathTransaction, stockCode + ".txt")
        self.stockCode = stockCode

    def run(self) -> []:
        if not os.path.exists(self.pathQuotationFile):
            logger.error(self.pathQuotationFile + "不存在")
            raise IOError(self.pathQuotationFile + "不存在")
        if not os.path.exists(self.pathTransactionFile):
            logger.error(self.pathTransactionFile + "不存在")
            raise IOError(self.pathTransactionFile + "不存在")
        quotation_file = open(self.pathQuotationFile)
        matching_list = []
        transaction_file = open(self.pathTransactionFile)
        logger.info("读取文件:"+self.pathQuotationFile)
        for line in quotation_file:
            quotation_bean = json.loads(line)
            if 93000000 <= int(quotation_bean["packetTime"]) <= 113000000 or 130000000 <= int(
                    quotation_bean["packetTime"]) <= 150005000:
                matching_list.append(MatchingBean(quotation_bean))
        i = 0
        logger.info("读取文件:" + self.pathTransactionFile)
        for line in transaction_file:
            transaction_bean = json.loads(line)
            if int(transaction_bean["tradeTime"]) <= 92500000:
                continue
            while i < len(matching_list) and \
                    int(transaction_bean["tradeTime"]) >= int(matching_list[i].quotation["packetTime"]):
                i += 1
            if i > len(matching_list)-1:
                break
            matching_list[i].transaction_list.append(transaction_bean)
        self.matchingList = matching_list
        return matching_list


class MatchingWorkBuilder(object):
    """
    匹配单元创建类
    构造器需要传入行情文件地址和逐笔文件地址
    """
    def __init__(self, pathQuotation, pathTransaction):
        if not isinstance(pathQuotation, str):
            raise ValueError('行情文件地址必须为字符串')
        if not isinstance(pathTransaction, str):
            raise ValueError('逐笔文件地址必须为字符串')
        if len(pathQuotation) == 0:
            raise ValueError('行情文件地址不能为空')
        if len(pathTransaction) == 0:
            raise ValueError('逐笔文件地址不能为空')
        self.pathQuotation = pathQuotation
        self.pathTransaction = pathTransaction
    """
    匹配单元创建方法
    方法参数需要传入待匹配股票代码
    """
    def create_worker(self, stockCode) -> MatchingWorker:
        if not isinstance(stockCode, str):
            raise ValueError('股票代码必须为字符串')
        if not len(stockCode) == 6:
            raise ValueError('股票代码必须6位')
        return MatchingWorker(self.pathQuotation, self.pathTransaction, stockCode)


class MatchingBean(object):
    """
    匹配结果类
    quotation是行情
    transaction_list是行情对应的逐笔
    """
    def __init__(self, quotation_dict):
        self.quotation = quotation_dict
        self.transaction_list = []

    def __str__(self):
        i = ""
        for transaction in self.transaction_list:
            i += transaction["tradeTime"]+"|"
        return 'stockCode:' + self.quotation["symbol"] + ',packetTime:' + self.quotation[
            "packetTime"] + ',transaction_list_size:' + str(len(self.transaction_list)) + ',transaction_list_times:'+ i


if __name__ == '__main__':
    builder = MatchingWorkBuilder("F:\\py\\StrategyFramework\\files\\quotation",
                                  "F:\\py\\StrategyFramework\\files\\transaction")
    worker = builder.create_worker("000001")
    data = worker.run()
    for match in data:
        print(match)
    print(data[0])
