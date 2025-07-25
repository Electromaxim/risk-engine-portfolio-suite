from .ch import SwissTradingCalendar
from .us import NYSETradingCalendar
from .jp import JPXTradingCalendar
from .hk import HKEXTradingCalendar

class GlobalTradingCalendar:
    REGION_CALENDARS = {
        "CH": SwissTradingCalendar(),
        "US": NYSETradingCalendar(),
        "UK": LSETradingCalendar(),  
        "JP": JPXTradingCalendar(),
        "HK": HKEXTradingCalendar()
    }
    
    def is_trading_day(self, date: date, region: str) -> bool:
        return self.REGION_CALENDARS[region].is_trading_day(date)