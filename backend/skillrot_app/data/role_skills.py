"""
skillrot_app/data/role_skills.py

Defines predefined tech roles and their associated skills in priority order.
Priority 1 = most critical for the role, Priority 5 = optional/nice-to-have.

Used by role_filter_service.py and the /skills/filter endpoint.
"""

from typing import Dict, List
from dataclasses import dataclass


@dataclass(frozen=True)
class RoleSkill:
    name: str
    priority: int  # 1 (Critical) → 5 (Optional)


ROLES: Dict[str, Dict] = {
    "software_engineering": {
        "label": "Software Engineering",
        "icon": "💻",
        "skills": [
            RoleSkill("Data Structures & Algorithms", 1),
            RoleSkill("System Design",                1),
            RoleSkill("JavaScript",                   2),
            RoleSkill("TypeScript",                   2),
            RoleSkill("Python",                       2),
            RoleSkill("React",                        3),
            RoleSkill("Node.js",                      3),
            RoleSkill("REST APIs",                    3),
            RoleSkill("SQL",                          3),
            RoleSkill("Git",                          4),
            RoleSkill("Docker",                       4),
            RoleSkill("CI/CD",                        4),
            RoleSkill("Testing",                      4),
            RoleSkill("Cloud AWS GCP Azure",          5),
            RoleSkill("Kubernetes",                   5),
            RoleSkill("GraphQL",                      5),
            RoleSkill("Redis",                        5),
            RoleSkill("Microservices",                5),
        ],
    },

    "cybersecurity": {
        "label": "Cybersecurity",
        "icon": "🔐",
        "skills": [
            RoleSkill("Network Security",        1),
            RoleSkill("Linux",                   1),
            RoleSkill("Penetration Testing",     2),
            RoleSkill("OWASP",                   2),
            RoleSkill("Cryptography",            2),
            RoleSkill("Incident Response",       3),
            RoleSkill("Malware Analysis",        3),
            RoleSkill("SIEM",                    3),
            RoleSkill("Threat Intelligence",     3),
            RoleSkill("Firewalls",               4),
            RoleSkill("Python Scripting",        4),
            RoleSkill("Reverse Engineering",     4),
            RoleSkill("Web App Security",        4),
            RoleSkill("Cloud Security",          5),
            RoleSkill("Forensics",               5),
            RoleSkill("Zero Trust",              5),
        ],
    },

    "data_science": {
        "label": "Data Science",
        "icon": "📊",
        "skills": [
            RoleSkill("Statistics",          1),
            RoleSkill("Python",              1),
            RoleSkill("Machine Learning",    2),
            RoleSkill("SQL",                 2),
            RoleSkill("Data Wrangling",      2),
            RoleSkill("Pandas",              3),
            RoleSkill("NumPy",               3),
            RoleSkill("Data Visualization",  3),
            RoleSkill("Feature Engineering", 3),
            RoleSkill("Deep Learning",       4),
            RoleSkill("NLP",                 4),
            RoleSkill("Model Deployment",    4),
            RoleSkill("A/B Testing",         4),
            RoleSkill("Spark",               5),
            RoleSkill("Computer Vision",     5),
            RoleSkill("MLOps",               5),
        ],
    },

    "devops": {
        "label": "DevOps",
        "icon": "⚙️",
        "skills": [
            RoleSkill("Linux Administration", 1),
            RoleSkill("Docker",               1),
            RoleSkill("CI/CD",                2),
            RoleSkill("Kubernetes",           2),
            RoleSkill("Terraform",            2),
            RoleSkill("Cloud Platforms",      3),
            RoleSkill("Ansible",              3),
            RoleSkill("Monitoring",           3),
            RoleSkill("Networking",           3),
            RoleSkill("Git",                  4),
            RoleSkill("Shell Scripting",      4),
            RoleSkill("Prometheus",           4),
            RoleSkill("Grafana",              4),
            RoleSkill("Helm",                 5),
            RoleSkill("Service Mesh",         5),
            RoleSkill("Cost Optimization",    5),
        ],
    },

    "web_development": {
        "label": "Web Development",
        "icon": "🌍",
        "skills": [
            RoleSkill("HTML",               1),
            RoleSkill("CSS",                1),
            RoleSkill("JavaScript",         1),
            RoleSkill("Responsive Design",  2),
            RoleSkill("React",              2),
            RoleSkill("TypeScript",         2),
            RoleSkill("REST APIs",          3),
            RoleSkill("Node.js",            3),
            RoleSkill("SQL",                3),
            RoleSkill("Web Performance",    4),
            RoleSkill("Accessibility",      4),
            RoleSkill("Authentication",     4),
            RoleSkill("Testing",            4),
            RoleSkill("Docker",             5),
            RoleSkill("Web Security",       5),
            RoleSkill("SEO",                5),
        ],
    },

    "ml_engineering": {
        "label": "ML Engineering",
        "icon": "🤖",
        "skills": [
            RoleSkill("Python",                  1),
            RoleSkill("Machine Learning",        1),
            RoleSkill("PyTorch",                 2),
            RoleSkill("TensorFlow",              2),
            RoleSkill("Data Pipelines",          2),
            RoleSkill("Model Training",          3),
            RoleSkill("Feature Stores",          3),
            RoleSkill("MLflow",                  3),
            RoleSkill("Model Serving",           3),
            RoleSkill("Docker",                  4),
            RoleSkill("Kubernetes",              4),
            RoleSkill("Cloud ML",                4),
            RoleSkill("Distributed Training",    4),
            RoleSkill("Monitoring",              5),
            RoleSkill("LLM Fine-tuning",         5),
            RoleSkill("Vector Databases",        5),
        ],
    },

    "full_stack_development": {
        "label": "Full Stack Dev",
        "icon": "🥞",
        "skills": [
            RoleSkill("JavaScript/TypeScript",   1),
            RoleSkill("React/Vue/Angular",       1),
            RoleSkill("Node.js/Python/Java",     1),
            RoleSkill("SQL/NoSQL Databases",     2),
            RoleSkill("REST/GraphQL APIs",       2),
            RoleSkill("HTML & CSS",              2),
            RoleSkill("Git & GitHub",            3),
            RoleSkill("Docker/Containers",       3),
            RoleSkill("CI/CD Pipelines",         4),
            RoleSkill("Cloud Deployments",       4),
            RoleSkill("Web Security",            5),
            RoleSkill("System Architecture",     5),
        ],
    },

    "mobile_development": {
        "label": "Mobile Dev",
        "icon": "📱",
        "skills": [
            RoleSkill("Swift/Kotlin",            1),
            RoleSkill("React Native/Flutter",    1),
            RoleSkill("Mobile UI/UX",            2),
            RoleSkill("State Management",        2),
            RoleSkill("REST APIs",               2),
            RoleSkill("App Store Deployment",    3),
            RoleSkill("Local Storage/SQLite",    3),
            RoleSkill("Push Notifications",      4),
            RoleSkill("Animations",              4),
            RoleSkill("Testing/QA",              5),
            RoleSkill("CI/CD Fastlane",          5),
        ],
    },

    "cloud_engineering": {
        "label": "Cloud Engineering",
        "icon": "☁️",
        "skills": [
            RoleSkill("AWS/GCP/Azure",           1),
            RoleSkill("Networking & VPC",        1),
            RoleSkill("IAM & Security",          2),
            RoleSkill("Infrastructure as Code",  2),
            RoleSkill("Docker & Kubernetes",     2),
            RoleSkill("Serverless Computing",    3),
            RoleSkill("Monitoring/CloudWatch",   3),
            RoleSkill("Linux Administration",    4),
            RoleSkill("Python/Bash Scripting",   4),
            RoleSkill("Cost Optimization",       5),
            RoleSkill("Disaster Recovery",       5),
        ],
    },

    "game_development": {
        "label": "Game Dev",
        "icon": "🎮",
        "skills": [
            RoleSkill("C++/C#",                  1),
            RoleSkill("Unity/Unreal Engine",     1),
            RoleSkill("3D Mathematics",          2),
            RoleSkill("Physics Engines",         2),
            RoleSkill("Rendering Pipeline",      3),
            RoleSkill("AI Behaviour Trees",      3),
            RoleSkill("Multiplayer/Networking",  4),
            RoleSkill("Performance Profiling",   4),
            RoleSkill("Audio Integration",       5),
            RoleSkill("Shaders",                 5),
        ],
    },
}

# Priority level metadata
PRIORITY_META: Dict[int, Dict] = {
    1: {"label": "Critical",  "description": "Must-have for the role"},
    2: {"label": "High",      "description": "Core competency"},
    3: {"label": "Medium",    "description": "Important supporting skill"},
    4: {"label": "Low",       "description": "Good to have"},
    5: {"label": "Optional",  "description": "Nice-to-have / specialization"},
}