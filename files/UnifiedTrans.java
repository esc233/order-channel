package com.bh.QuotationStorage.dto;

import lombok.Data;

import java.io.Serializable;
import java.util.List;

/**
 * 统一后的逐笔信息
 */
@Data
public class UnifiedTrans implements Serializable {
        /**
         * 数据日期 "dataDate": "20210402"
         */
        private String dataDate;


        /**
         * 成交价格 "tradePrice": 21.61
         */
        private String tradePrice;

        /**
         * 成交时间 深圳: 20210402101220560  上海：101220370，统一为tick中的格式：101220370
         */
        private String tradeTime;

        /**
         * 成交数量 "tradeVolume": 100
         */
        private String tradeVolume;


        /**
         * 成交金额 "tradeAmount": 19458,
         */
        private String tradeAmount;

        /**
         * 买方订单号
         */
        private String buyRecId;

        /**
         * 卖方订单号
         */
        private String sellRecId;
}
