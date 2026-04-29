const resumeData = {
  name: 'Hasnain Asif',
  titles: ['AI Engineer', 'Agentic AI & LLM Systems', 'Full-Stack Engineer'],

  contact: [
    {
      type: 'email',
      label: 'hasnainsaf52@gmail.com',
      href: 'mailto:hasnainsaf52@gmail.com',
    },
    { type: 'phone', label: '+92 301 371 6896', href: 'tel:+923013716896' },
    {
      type: 'linkedin',
      label: 'linkedin.com/in/hasnain-asif',
      href: 'https://linkedin.com/in/hasnain-asif',
    },
    {
      type: 'github',
      label: 'github.com/HasnainAsif',
      href: 'https://github.com/HasnainAsif',
    },
    {
      type: 'website',
      label: 'hasnainasif.vercel.app',
      href: 'https://hasnainasif.vercel.app',
    },
    { type: 'location', label: 'Lahore, Pakistan' },
  ],

  summary:
    'AI Engineer with 5+ years of full-stack development experience, specialized in agentic AI systems, RAG pipelines, and LLM integrations deployed on AWS. Built multi-agent LangGraph pipelines, autonomous task execution systems, and enterprise-scale web platforms serving 11,000+ users across 4 countries.',

  skills: [
    {
      category: 'AI & LLM',
      tags: [
        'Python',
        'LangChain',
        'LangGraph',
        'LlamaIndex',
        'CrewAI',
        'OpenAI Agents SDK',
        'Vector Databases',
        'LLMs',
        // "Large Language Models (LLMs)",
        'Retrieval-Augmented Generation (RAG)',
        'Transformer',
        // "Machine Learning",
        'ML',
        'NLP',
        'Prompt Engineering',
        'Embeddings',
        'Multi-Agent Systems',
        'FastAPI',
      ],
    },
    {
      category: 'Cloud & DevOps',
      tags: [
        'AWS Lambda',
        'SQS',
        'EventBridge',
        'API Gateway',
        'Bedrock',
        'SageMaker',
        'S3 / ECR',
        'Terraform',
        'GitHub Actions',
        'Docker',
        'CI/CD',
      ],
    },
    {
      category: 'Full-Stack',
      tags: [
        'React',
        'Next.js',
        'Node.js',
        'TypeScript',
        'Express.js',
        'Web3.js',
        'Redux',
        'GraphQL',
        'WebSockets',
        'Microservices',
        'REST API',
        'Agile',
        'Scrum',
      ],
    },
    {
      category: 'Databases',
      tags: ['PostgreSQL', 'MongoDB', 'ChromaDB', 'FAISS', 'Pinecone', 'Redis'], // "Semantic Search", "BM25",
    },
  ],

  experience: [
    {
      role: 'AI Engineer — Agentic AI & Production Systems',
      date: 'Oct 2025 – Present',
      company: 'Self-Employed · Independent AI Engineer',
      subtitle:
        'Designing and developing production agentic AI systems — multi-agent pipelines, RAG architectures, and LLM integrations deployed on AWS.',
      bullets: [
        'Built an agentic RAG pipeline with a retrieval evaluator agent that filters documents by relevance before generation — improving answer quality in document-heavy use cases.',
        'Deployed a distributed multi-agent system on AWS: five Lambda functions (one per agent), S3-backed vector storage, SageMaker embeddings, API Gateway orchestration, and CloudFront + S3 for a Next.js frontend.',
        'Deployed IaC pipelines using Terraform and GitHub Actions for automated deployment across AWS Bedrock, Lambda, ECR, S3, and CloudFront.',
      ],
    },
    {
      role: 'Senior Software Engineer',
      date: 'Oct 2023 – Present',
      company: 'tkxel · Lahore, Pakistan',
      subtitle:
        'Worked on enterprise-scale systems for US-based clients, including workforce platforms and multi-tenant SaaS products.',
      bullets: [
        'Led a 5-engineer team to revive a 2-year abandoned multi-tenant social platform with no documentation — owned task breakdown, PR reviews, and all technical decisions.',
        'Built the scheduling, shift assignment, and DST timezone engine for an enterprise workforce platform — adopted across 50+ components, serving 11,000+ users across 170+ franchises in 4 countries, with invalid assignments blocked at UI level to prevent payroll errors.',
        'Reverse-engineered OpenFGA authorization schema from legacy deployments — restored full role-based access control across all admin levels; separately shipped multi-currency Stripe subscriptions (PKR, USD, GBP) on a platform designed for 1M+ audience members across 1,000–5,000 brand Hubs.',
      ],
    },
    {
      role: 'Software Engineer',
      date: 'May 2022 – Oct 2023',
      company: 'tkxel · Lahore, Pakistan',
      subtitle:
        'Built full-stack features for enterprise tools and internal platforms.',
      bullets: [
        'Delivered enterprise helpdesk features for Tikit, an MS Teams-integrated ticketing platform for high-volume IT, HR, and Finance workflows.',
        'Developed a Custom Views system for an MS Teams-integrated enterprise helpdesk — enabled persistent multi-filter configurations across thousands of concurrent tickets.',
      ],
    },
    {
      role: 'Software Engineer',
      date: 'Oct 2021 – Jan 2022',
      company: 'Invozone · Lahore, Pakistan',
      subtitle:
        'Frontend-led delivery on a multi-chain DEX product for a Web3 startup — cross-chain token swaps across four networks using Web3 infrastructure.',
      bullets: [
        'Directed frontend delivery on a multi-chain DEX across Ethereum, BSC, Polygon, and Avalanche — integrated MetaMask and Coinbase wallets via Web3.js.',
      ],
    },
    {
      role: 'Software Engineer',
      date: 'Aug 2020 – Oct 2021',
      company: 'OptimusFox · Lahore, Pakistan',
      subtitle:
        'Built full-stack blockchain-based platforms across fintech and civic tech — led delivery on multiple products.',
      bullets: [
        'Served as tech lead on a token offering (ITO) platform — designed ERD, owned full-stack architecture, and routed tasks across a 4-engineer team.',
        'Built a blockchain-based tamper-resistant e-voting system with three role-based panels — admin, candidate, and voter — with on-chain ballot execution via Web3.js.',
      ],
    },
  ],

  projects: [
    {
      active: true,
      name: 'DocInsight — Verified Document Q&A',
      stack: 'LangGraph · LangChain · ChromaDB · OpenAI · FastAPI',
      desc: 'A multi-agent RAG system that eliminates manual document review — three specialized agents gate relevance, generate grounded answers, and verify factual support before any response reaches the user. Targets the 1.8 hours/day that knowledge workers lose to unverified information retrieval.',
      bullets: [
        'Built a 3-agent LangGraph pipeline with OpenAI — Relevance Checker, Research Agent, and Verification Agent — answers verified against source passages before being returned to the user.',
        'Implemented hybrid retrieval combining BM25 (40%) and ChromaDB vector search (60%) — improves recall on exact-match queries that pure semantic search consistently misses.',
        'Designed conditional routing so failed verification triggers automatic re-research — unverified answers never surface to the user.',
      ],
    },
    {
      active: true,
      name: 'Sidekick — Autonomous AI Work Agent',
      stack: 'LangGraph · OpenAI · Playwright · Serper API · Python REPL',
      desc: 'A two-model agentic system that executes multi-step tasks across browser, code, files, and search without human supervision — a structurally independent evaluator verifies success criteria are met before any result is returned. Addresses the 62% of workday spent on tasks that could run unattended and the 9.5 minutes of focus lost each time a worker checks in on a running task.',
      bullets: [
        'Built a two-model LangGraph pipeline — worker executes across browser automation, Python REPL, file I/O, and web search, while a separate evaluator independently verifies task completion, eliminating self-evaluation bias.',
        'Implemented typed feedback loop — structured feedback is injected into the worker system prompt on retry, so the agent knows exactly why it failed before reattempting.',
        'Built a human-in-the-loop escalation mechanism — when the agent repeats the same mistake after feedback, it surfaces the blocker to the user instead of looping silently.',
      ],
    },
    {
      active: false,
      name: 'Enterprise Workforce Platform',
      stack: 'React · Node.js · MongoDB · Ruby on Rails · PostgreSQL · Azure',
      desc: 'Franchise-based security workforce management platform serving 11,000+ users across 170+ franchises in the US, Canada, UK, and Australia. Consolidated 5+ disconnected operational systems — scheduling, payroll, contracts, attendance, and invoicing — into a single unified platform.',
      bullets: [
        'Anchored all time logic to franchise location rather than browser or system settings — built a single DST layer handling inverted US/Australia cycles simultaneously, eliminating production shift drift across 50+ components.',
        'Designed frontend architecture with franchise-level data isolation built in — franchise users see only their operations while platform owners access global data across all 170+ franchises; isolation was architectural, not bolted on.',
        'Enforced contract boundaries at the UI level during shift assignment — supervisors operate within contract hours and shift states with invalid assignments blocked before they reach payroll.',
      ],
    },
    {
      active: false,
      name: 'Multi-Tenant Social Platform',
      stack: 'React · Node.js · GraphQL · MongoDB · OpenFGA · Stripe · AWS',
      desc: 'Managed a 5-engineer team for 4 months to revive an abandoned multi-tenant social platform inactive for 2 years — restored a fully non-functional system with no documentation, no infrastructure visibility, and no prior ownership handoff.',
      bullets: [
        'Spent 1 month reverse-engineering OpenFGA tuple relationships from broken production deployments — reconstructed Super Admin, Organization Admin, and sub-admin permission hierarchies entirely without documentation.',
        'Recovered broken AWS infrastructure (S3, Lambda, ECS) with no prior ownership context — restored core platform workflows including org/hub/circle creation, content management, and audience engagement.',
        'Built Stripe multi-currency subscription flow — admins configure pricing per circle in PKR, USD, and GBP simultaneously; audience members subscribe in preferred currency on a platform with zero prior working monetization.',
      ],
    },
  ],

  education: [
    {
      degree: 'BS Software Engineering',
      school: 'University of Engineering & Technology, Taxila',
      location: 'Rawalpindi, Pakistan',
    },
  ],

  certifications: [
    { name: 'IBM RAG and Agentic AI Specialization', issuer: 'Coursera · IBM' },
    {
      name: 'AI Engineer Production Track: Deploy LLMs & Agents at Scale',
      issuer: 'Udemy · Ed Donner',
    },
    {
      name: 'Agentic Track: The Complete Agent & MCP Course',
      issuer: 'Udemy · Ed Donner',
    },
    {
      name: 'Serverless Framework Bootcamp: Node.js, AWS & Microservices',
      issuer: 'Udemy · Ariel Weinberger',
    },
    {
      name: 'Data Science Internship Certificate',
      issuer: 'Skilled Score · Gufhtugu Publications',
    },
  ],

  // achievements section is currently disabled — set active: true to re-enable
  achievements: {
    active: false,
    items: [
      {
        icon: '🌍',
        strong: '11,000+ Users, 4 Countries:',
        text: 'Delivered and maintained an enterprise workforce platform across 170+ franchises in the US, Canada, UK, and Australia without production downtime.',
      },
      {
        icon: '⏱',
        strong: 'Zero Scheduling Errors:',
        text: 'Designed a location-anchored DST timezone engine adopted across 50+ components — eliminated all production-level shift scheduling errors for a globally distributed user base.',
      },
      {
        icon: '🔄',
        strong: 'Revived a Dead Platform:',
        text: 'Led a 5-engineer team to fully restore a 2-year abandoned multi-tenant social platform with no documentation, no infrastructure visibility, and no handoff — shipping live in 4 months.',
      },
      {
        icon: '🤖',
        strong: 'Production Agentic AI:',
        text: 'Built and deployed a distributed multi-agent system on AWS — five independent Lambda agents with S3-backed vector storage, SageMaker embeddings, and full IaC via Terraform.',
      },
      {
        icon: '💳',
        strong: 'Multi-Currency Payments at Scale:',
        text: 'Shipped Stripe subscription billing in PKR, USD, and GBP on a platform designed for 1M+ audience members across 1,000–5,000 brand Hubs.',
      },
    ],
  },
};
