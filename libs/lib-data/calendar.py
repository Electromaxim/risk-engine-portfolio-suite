class GlobalTradingCalendar:  
    REGIONS = {  
        "CH": SwissTradingCalendar(),  
        "US": NYSETradingCalendar(),  
        "UK": LSETradingCalendar(),  
        "JP": JPXTradingCalendar(),  
        "HK": HKEXTradingCalendar()  
    }  

    def is_trading_day(self, date: date, region: str = "CH") -> bool:  
        return self.REGIONS[region].is_trading_day(date)  