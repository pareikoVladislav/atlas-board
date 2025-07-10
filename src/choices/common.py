from enum import Enum, StrEnum


class Priority(tuple, Enum):
    LOW = 5, 'Low'
    MEDIUM = 4, 'Medium'
    HIGH = 3, 'High'
    VERY_HIGH = 2, 'Very High'
    URGENT = 1, 'Urgent'

    @classmethod
    def choices(cls):
        return [(attr.value[0], attr.value[1]) for attr in cls]


class Position(StrEnum):
    CEO = "CEO"
    CTO = "CTO"
    DESIGNER = "Designer"
    PRODUCT_OWNER = "Product Owner"
    PROJECT_OWNER = "Project Owner"
    BACKEND_DEVELOPER = "Backend Developer"
    FRONTEND_DEVELOPER = "Frontend Developer"
    IOS_DEVELOPER = "iOS Developer"
    MOBILE_DEVELOPER = "Mobile Developer"
    DEVOPS_ENGINEER = "DevOps Engineer"
    DATA_SCIENTIST = "Data Scientist"
    DATA_ENGINEER = "Data Engineer"
    DATABASE_ADMIN = "Database Admin"
    ML_ENGINEER = "ML Engineer"
    PROJECT_MANAGER = "Project Manager"
    QA = "QA"

    @classmethod
    def choices(cls):
        return[(attr.value.upper(), attr.value) for attr in cls]
