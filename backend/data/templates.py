
# Sample project templates database
PROJECT_TEMPLATES = {
    'music': {
        'name': 'Music Data Visualizer',
        'description': 'Interactive visualization of audio data with ML-based genre analysis',
        'languages': ['Python', 'JavaScript'],
        'skills_gained': ['Audio Analysis', 'Data Visualization', 'ML Fundamentals'],
        'difficulty': 'Intermediate',
        'steps': [
            {
                'title': 'Setup audio processing',
                'description': 'Install librosa and process audio files',
                'duration': '2 hours',
                'resources': ['https://librosa.org/doc/latest/index.html']
            },
            {
                'title': 'Create visualizations',
                'description': 'Use matplotlib/plotly for waveforms and spectrograms',
                'duration': '3 hours',
                'resources': ['https://matplotlib.org/stable/gallery/index.html']
            },
            {
                'title': 'Add interactivity',
                'description': 'Build Dash/Streamlit interface',
                'duration': '4 hours',
                'resources': ['https://dash.plotly.com/']
            },
            {
                'title': 'Implement ML',
                'description': 'Train genre classifier with sklearn',
                'duration': '5 hours',
                'resources': ['https://scikit-learn.org/']
            }
        ],
        'neuroplasticity': 'Combines auditory processing with technical skills, strengthening neural pathways between creative and analytical thinking. This cross-domain integration enhances long-term memory retention by 40%.'
    },
    'gaming': {
        'name': 'Gaming Stats Tracker',
        'description': 'Real-time performance analytics dashboard for competitive gaming',
        'languages': ['JavaScript', 'Python'],
        'skills_gained': ['API Integration', 'Real-time Data', 'Dashboard Design'],
        'difficulty': 'Intermediate',
        'steps': [
            {
                'title': 'API research',
                'description': 'Explore gaming APIs (Riot, Steam, Discord)',
                'duration': '2 hours',
                'resources': ['https://developer.riotgames.com/']
            },
            {
                'title': 'Data pipeline',
                'description': 'Fetch and store player statistics',
                'duration': '4 hours',
                'resources': ['https://docs.python-requests.org/']
            },
            {
                'title': 'Build dashboard',
                'description': 'Create React/Vue dashboard with charts',
                'duration': '5 hours',
                'resources': ['https://recharts.org/']
            },
            {
                'title': 'Add analytics',
                'description': 'Performance trends and predictions',
                'duration': '4 hours',
                'resources': ['https://www.chartjs.org/']
            }
        ],
        'neuroplasticity': 'Transforms gaming passion into data literacy, activating reward pathways through personally meaningful projects. Intrinsic motivation increases skill retention by 60%.'
    },
    'robotics': {
        'name': 'Robotics Simulation Platform',
        'description': 'Physics-based robot control and path planning simulator',
        'languages': ['Python', 'C++'],
        'skills_gained': ['Physics Simulation', 'Control Systems', '3D Graphics'],
        'difficulty': 'Advanced',
        'steps': [
            {
                'title': 'Setup PyBullet',
                'description': 'Install physics engine and load basic robots',
                'duration': '3 hours',
                'resources': ['https://pybullet.org/']
            },
            {
                'title': 'Implement controls',
                'description': 'PID controllers for movement',
                'duration': '5 hours',
                'resources': ['https://en.wikipedia.org/wiki/PID_controller']
            },
            {
                'title': 'Path planning',
                'description': 'A* algorithm for navigation',
                'duration': '4 hours',
                'resources': ['https://www.redblobgames.com/pathfinding/a-star/']
            },
            {
                'title': 'Visualization',
                'description': 'Real-time 3D rendering with OpenGL',
                'duration': '4 hours',
                'resources': ['https://learnopengl.com/']
            }
        ],
        'neuroplasticity': 'Engages spatial reasoning and systems thinking, building connections between abstract concepts and physical understanding. Multimodal learning strengthens hippocampal encoding.'
    },
    'photography': {
        'name': 'AI-Powered Photo Organizer',
        'description': 'Automatic photo categorization and enhancement using computer vision',
        'languages': ['Python', 'JavaScript'],
        'skills_gained': ['Computer Vision', 'Deep Learning', 'UI Design'],
        'difficulty': 'Intermediate',
        'steps': [
            {
                'title': 'Setup CV pipeline',
                'description': 'Install OpenCV and load pretrained models',
                'duration': '3 hours',
                'resources': ['https://opencv.org/']
            },
            {
                'title': 'Object detection',
                'description': 'Implement YOLO for scene classification',
                'duration': '5 hours',
                'resources': ['https://pjreddie.com/darknet/yolo/']
            },
            {
                'title': 'Build interface',
                'description': 'Create drag-and-drop photo gallery',
                'duration': '4 hours',
                'resources': ['https://react-dropzone.js.org/']
            },
            {
                'title': 'Auto-enhancement',
                'description': 'Apply filters and adjustments using ML',
                'duration': '4 hours',
                'resources': ['https://pillow.readthedocs.io/']
            }
        ],
        'neuroplasticity': 'Merges artistic vision with technical implementation, activating both visual cortex and logical processing centers. Creative-technical integration promotes cognitive flexibility.'
    },
    'finance': {
        'name': 'Personal Finance Dashboard',
        'description': 'Budget tracking and investment portfolio analyzer',
        'languages': ['Python', 'JavaScript'],
        'skills_gained': ['Data Analysis', 'API Integration', 'Financial Modeling'],
        'difficulty': 'Beginner',
        'steps': [
            {
                'title': 'Data collection',
                'description': 'Connect to financial APIs (Plaid, Alpha Vantage)',
                'duration': '3 hours',
                'resources': ['https://plaid.com/docs/']
            },
            {
                'title': 'Budget analyzer',
                'description': 'Categorize expenses and create insights',
                'duration': '4 hours',
                'resources': ['https://pandas.pydata.org/']
            },
            {
                'title': 'Visualization',
                'description': 'Build interactive charts for spending patterns',
                'duration': '3 hours',
                'resources': ['https://plotly.com/python/']
            },
            {
                'title': 'Investment tracker',
                'description': 'Portfolio performance and predictions',
                'duration': '5 hours',
                'resources': ['https://www.alphavantage.co/']
            }
        ],
        'neuroplasticity': 'Personal financial data creates emotional investment in learning, triggering stronger memory consolidation through relevance and immediate applicability.'
    }
}

RESEARCH_TEMPLATES = [
    {
        'title': 'Neuroplasticity in Skill Acquisition Through Project-Based Learning',
        'difficulty': 'Intermediate',
        'skills': ['Neuroscience', 'Education Theory', 'Data Analysis'],
        'description': 'Investigate how hands-on projects create stronger neural pathways compared to traditional learning methods. Study synaptic strengthening through active engagement.',
        'keywords': ['neuroplasticity', 'learning', 'education']
    },
    {
        'title': 'AI-Driven Personalized Career Path Optimization',
        'difficulty': 'Advanced',
        'skills': ['Machine Learning', 'Career Science', 'NLP'],
        'description': 'Develop algorithms that map individual interests to optimal career trajectories using graph neural networks and reinforcement learning.',
        'keywords': ['ai', 'career', 'optimization', 'machine learning']
    },
    {
        'title': 'Identity-Aligned Motivation in Technical Education',
        'difficulty': 'Intermediate',
        'skills': ['Psychology', 'EdTech', 'Survey Design'],
        'description': 'Study correlation between personal interest integration and learning outcomes in STEM fields. Examine intrinsic vs extrinsic motivation effects.',
        'keywords': ['motivation', 'education', 'psychology']
    },
    {
        'title': 'Computer Vision Applications in Creative Industries',
        'difficulty': 'Advanced',
        'skills': ['Deep Learning', 'Computer Vision', 'Design'],
        'description': 'Explore how CV techniques can augment creative workflows in photography, videography, and digital art.',
        'keywords': ['computer vision', 'creative', 'photography', 'art']
    },
    {
        'title': 'Real-Time Data Processing for Gaming Analytics',
        'difficulty': 'Intermediate',
        'skills': ['Data Engineering', 'Gaming', 'Statistics'],
        'description': 'Build scalable pipelines for processing millions of gaming events per second with low latency.',
        'keywords': ['gaming', 'data', 'real-time']
    },
    {
        'title': 'Robotics Simulation Accuracy and Transfer Learning',
        'difficulty': 'Advanced',
        'skills': ['Robotics', 'Simulation', 'Machine Learning'],
        'description': 'Research sim-to-real transfer techniques to minimize the reality gap in robotic control systems.',
        'keywords': ['robotics', 'simulation', 'machine learning']
    }
]