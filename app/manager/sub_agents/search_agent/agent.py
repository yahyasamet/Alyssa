from google.adk.agents import Agent
from google.adk.tools import google_search

# def get_current_time() -> dict:
#     """
#     Get the current time in the format YYYY-MM-DD HH:MM:SS
#     """
#     return {
#         "current_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
#     }

search_agent = Agent(
    name="search_agent",
    model="gemini-2.0-flash-exp",
    description="Agent to help with searching the web for information.",
    instruction="""
    أنت مساعد مفيد يمكنه استخدام الأدوات التالية:
    - google_search: للبحث في الويب عن المعلومات
    
    ## اللغة والتفاعل
    - **اللغة الافتراضية**: تحدث باللغة العربية (اللهجة السعودية) بشكل افتراضي
    - **التبديل الديناميكي**: إذا طلب المستخدم التحدث بلغة أخرى، انتقل فوراً إلى تلك اللغة
    - **الحفاظ على السياق**: احتفظ بفهم السياق عند التبديل بين اللغات
    
    ## إرشادات البحث
    - قم بتنفيذ عمليات البحث على الويب باستخدام google_search
    - قدم نتائج شاملة ومفيدة للمستخدم
    - لخص المعلومات المهمة من نتائج البحث
    - اذكر مصادر المعلومات عند الحاجة
    
    إذا سأل المستخدم عن أي شيء آخر غير متعلق بالبحث، 
    يجب عليك تفويض المهمة إلى الوكيل المدير.
    """,
    tools=[google_search],
    # tools=[get_current_time],
    # tools=[google_search, get_current_time], # <--- Doesn't work
)