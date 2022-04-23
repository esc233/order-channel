package com.bh.QuotationStorage.dto;

import lombok.Data;
import java.io.Serializable;
import java.util.List;

/**
 * 接收到的行情推送信息
 */
@Data
public class ReceivedTick implements Serializable {
    private String symbol;

    private String dataDate;

    private String packetTime;

    private String status;

    private String preClosePrice;

    private String openPrice;

    private String highPrice;

    private String lowPrice;

    private String lastPrice;

    private String closePrice;

    private String totalNo;

    private String totalAmount;

    private String totalVolume;

    private String totalBuyOrderVolume;

    private String totalSellOrderVolume;

    private List<SellBuyInfo> sellPriceList;

    private List<SellBuyInfo> buyPriceList;
}
