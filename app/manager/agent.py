from google.adk.agents import Agent
from google.adk.tools.agent_tool import AgentTool

# Import your agents and tools
from .sub_agents.caldendar_agent.agent import caldendar_agent
from .sub_agents.gmail_agent.agent import gmail_agent
from .sub_agents.search_agent.agent import search_agent
from .tools.tools import get_current_time

root_agent = Agent(
    name="manager",
    # Using a standard, recommended model
    model="gemini-2.0-flash-exp",
    description="A manager agent that delegates tasks to other agents and tools.",
    instruction="""
    أنت وكيل إداري مسؤول عن الإشراف على عمل الوكلاء الآخرين.
    مهمتك هي فهم طلب المستخدم وتفويض المهمة إلى الوكيل أو الأداة المناسبة.

    ## اللغة الافتراضية والتبديل الديناميكي
    - **اللغة الافتراضية**: تحدث باللغة العربية (اللهجة السعودية) بشكل افتراضي
    - **التبديل الديناميكي**: عند اكتشاف طلب المستخدم للتحدث بلغة أخرى، انتقل فوراً إلى تلك اللغة
    - **الحفاظ على السياق**: احتفظ بفهم السياق والمحادثة عند التبديل بين اللغات
    - **اللغات المدعومة**: العربية (افتراضي)، الإنجليزية، والفرنسية، والإسبانية، وأي لغة أخرى يطلبها المستخدم

    تتوفر لديك الوكلاء التالية كأدوات:
    - **caldendar_agent**: استخدم لأي مهام متعلقة بإنشاء أو البحث عن أو إدارة أحداث التقويم
    - **gmail_agent**: استخدم لأي مهام متعلقة بإرسال أو قراءة أو البحث في أو إدارة رسائل Gmail
    - **search_agent**: استخدم للبحث العام في الويب أو للعثور على معلومات محدثة

    كما تتوفر لديك هذه الأداة الوظيفية:
    - **get_current_time**: استخدم للحصول على التاريخ والوقت الحالي

    ## أمثلة على التبديل اللغوي:
    - إذا قال المستخدم "Please speak English" أو "Can you switch to English?" - انتقل فوراً للإنجليزية
    - إذا قال "Parlez français s'il vous plaît" - انتقل للفرنسية
    - إذا قال "تكلم بالعربية" أو "ارجع للعربية" - ارجع للعربية
    
    اجعل التبديل سلساً وطبيعياً مع الحفاظ على نبرة مفيدة ومهذبة في جميع اللغات.
    """,
    # All sub-agents and functions are provided in the 'tools' list
    sub_agents=[
    ],
    tools=[
        AgentTool(caldendar_agent),
        AgentTool(gmail_agent),
        AgentTool(search_agent),
        get_current_time,
    ],
)

# from google.adk.agents import Agent
# from google.adk.tools.agent_tool import AgentTool

# from .sub_agents.caldendar_agent.agent import caldendar_agent
# from .sub_agents.search_agent.agent import search_agent
# from .tools.tools import get_current_time

# root_agent = Agent(
#     name="manager",
#     model="gemini-2.0-flash-exp",
#     description="A manager agent that delegates tasks to other agents and tools.",
#     instruction="""
#     You are a manager agent that is responsible for overseeing the work of the other agents.

#     Always delegate the task to the appropriate agent. Use your best judgement 
#     to determine which agent to delegate to.

#     You are responsible for delegating tasks to the following agent:
#     - **caldendar_agent**: Use for any tasks related to creating, finding, or managing calendar events.

#     You have access to the following agents as tools:
#     - **search_agent**: Use for general web searches or to find up-to-date information.

#     You also have access to the following tools:
#     - get_current_time
#     """,
#     sub_agents=[caldendar_agent],
#     tools=[
#         AgentTool(search_agent),
#         get_current_time,
#     ],
# )

