export interface Education {
  degree: string;
  field: string;
  institution: string;
  location: string;
  expectedGraduation: string;
  status: string;
}

export interface HeroData {
  name: string;
  tagline: string;
  subline: string;
  ctaPrimary: {
    label: string;
    target: string;
  };
  ctaSecondary: {
    label: string;
    href: string;
  };
  stats: {
    label: string;
    value: string;
  }[];
}

export interface AboutData {
  title: string;
  summary: string;
  education: Education;
  keyHighlights: string[];
}

export interface SkillCategory {
  id: string;
  category: string;
  iconName: string;
  description: string;
  skills: string[];
}

export interface ExperienceItem {
  id: string;
  role: string;
  company: string;
  location: string;
  period: string;
  durationHours: string;
  bullets: string[];
  technologies: string[];
}

export interface ProjectItem {
  id: string;
  title: string;
  subtitle: string;
  category: "Team Project" | "Independent Project" | "Future Slot";
  description: string;
  highlights: string[];
  subsystemRole?: string;
  tools: string[];
  specificsTag: string;
  isEmptySlot?: boolean;
}

export interface ContactData {
  title: string;
  subtitle: string;
  phone: string;
  email: string;
  location: string;
  resumeUrl: string;
  socials: {
    platform: string;
    href: string;
    icon: string;
  }[];
}

export interface PortfolioContent {
  hero: HeroData;
  about: AboutData;
  skills: SkillCategory[];
  experience: ExperienceItem[];
  projects: ProjectItem[];
  contact: ContactData;
}

export const portfolioContent: PortfolioContent = {
  hero: {
    name: "Pranav S",
    tagline: "Mechatronics Engineering Student — PLC Programming, Mechanical Design & Robotics",
    subline: "Based in Vellore, Tamil Nadu, India",
    ctaPrimary: {
      label: "View Projects",
      target: "#projects",
    },
    ctaSecondary: {
      label: "Download Resume",
      href: "/resume.pdf",
    },
    stats: [
      { label: "Internship Hours", value: "208+" },
      { label: "CAD Suite Proficiency", value: "4 Tools" },
      { label: "Robotics Competitions", value: "Robocon '25" },
    ],
  },

  about: {
    title: "About Me",
    summary:
      "Mechatronics engineering student with hands-on experience in PLC programming, electrical panel building, and mechanical design across AutoCAD, Fusion 360, SolidWorks, and Autodesk Inventor. Practical robotics exposure through Robocon 2025 and an independently built Automated Guided Vehicle (AGV). Combines strong design and fabrication skills with a structured, detail-oriented approach to engineering problems.",
    education: {
      degree: "Bachelor of Engineering (B.E.)",
      field: "Mechatronics Engineering",
      institution: "Kumaraguru College of Technology",
      location: "Coimbatore, Tamil Nadu",
      expectedGraduation: "Expected 2028",
      status: "Undergraduate",
    },
    keyHighlights: [
      "Industrial Control & PLC Ladder Logic Programming",
      "Multi-CAD Mechanical Modeling & 3D Prototyping",
      "Electrical Control Panel Hardware Wiring & Schematics",
      "Autonomous Robot Kinematics & AGV Systems Integration",
    ],
  },

  skills: [
    {
      id: "cad-mechanical",
      category: "CAD & Mechanical Design",
      iconName: "Compass",
      description: "Comprehensive 3D parametric modeling, drafting, and assembly analysis.",
      skills: ["AutoCAD", "Fusion 360", "SolidWorks", "Autodesk Inventor"],
    },
    {
      id: "automation-plc",
      category: "Automation / PLC",
      iconName: "Cpu",
      description: "Industrial automation software logic, sequence control, and safety circuits.",
      skills: [
        "Delta WPLSoft",
        "Ladder Logic",
        "Timers & Counters",
        "SET / RST Latch Functions",
      ],
    },
    {
      id: "electrical-systems",
      category: "Electrical Systems",
      iconName: "Zap",
      description: "Hardware integration, wiring schematics, relay logic, and panel construction.",
      skills: [
        "Electrical Panel Building",
        "Hardware Systems Integration",
        "Control Circuit Wiring",
        "Power & Signal Distribution",
      ],
    },
    {
      id: "fabrication",
      category: "Fabrication & Prototyping",
      iconName: "Hammer",
      description: "Hands-on machine fabrication, physical prototyping, and chassis assembly.",
      skills: [
        "Hands-on Fabrication",
        "Rapid Prototyping",
        "Mechanical Assembly",
        "Materials & Tolerances",
      ],
    },
  ],

  experience: [
    {
      id: "suntech-internship",
      role: "PLC Programming & Design Intern",
      company: "Suntech Energreen Private Limited",
      location: "Arni, Tamil Nadu",
      period: "June 2026",
      durationHours: "208 Hours",
      bullets: [
        "Completed a structured 208-hour internship spanning PLC programming, electrical panel building, and 3D mechanical design.",
        "Developed and tested ladder logic programs using Delta WPLSoft under the guidance of the Engineering Technical Manager.",
        "Assisted in electrical panel building and control circuit wiring for industrial automation systems.",
        "Applied CAD software tools to 3D mechanical design, chassis components, and assembly modeling tasks.",
      ],
      technologies: ["Delta WPLSoft", "Ladder Logic", "Panel Wiring", "AutoCAD", "3D CAD Modeling"],
    },
  ],

  projects: [
    {
      id: "robocon-2025",
      title: "Robocon 2025 Robot",
      subtitle: "National-Level Robotics Competition",
      category: "Team Project",
      description:
        "Part of a competitive engineering team that designed and fabricated a custom competition robot engineered for high-precision autonomous and manual challenge tasks.",
      subsystemRole: "Mechanical Design & Fabrication Subsystem Lead",
      highlights: [
        "Co-designed structural chassis geometry in CAD to optimize weight distribution and structural rigidity.",
        "Fabricated custom mounting brackets and actuator drive linkages under strict competition dimensional constraints.",
        "Integrated sensor mounts and wire routing channels to ensure high operational reliability on the field.",
      ],
      tools: ["Fusion 360", "SolidWorks", "Prototyping", "Actuators & Sensors"],
      specificsTag: "Subsystem: Chassis & Drive Mechanism | Role: Mechanical Lead",
    },
    {
      id: "agv-vehicle",
      title: "AGV — Automated Guided Vehicle",
      subtitle: "Independent Robotics & Automation Build",
      category: "Independent Project",
      description:
        "Independently designed, engineered, and constructed an Automated Guided Vehicle (AGV) incorporating custom mechanical chassis layout, sensors, and automation logic.",
      subsystemRole: "Solo Engineer (Design, Wiring, Programming & Testing)",
      highlights: [
        "Engineered custom chassis drive kinematics and wheel mounts in SolidWorks / Fusion 360.",
        "Wired motor controllers, power distribution boards, and optical/ultrasonic guidance sensors.",
        "Implemented autonomous navigation logic and obstacle detection algorithms for reliable line and path following.",
      ],
      tools: ["AutoCAD", "Fusion 360", "Automation Sensors", "Motor Controllers", "Prototyping"],
      specificsTag: "Sensors: IR Line Trackers & Ultrasonic | Nav: Autonomous Guidance",
    },
    {
      id: "future-project-slot",
      title: "Upcoming Project Slot",
      subtitle: "Reserved for Next Innovation",
      category: "Future Slot",
      description:
        "Reserved slot ready for future mechatronics, industrial automation, or robotics projects as new designs and research develop.",
      highlights: [
        "Configured for seamless addition of new technical case studies, CAD models, or PLC implementations without layout changes.",
      ],
      tools: ["Mechatronics", "Automation", "Embedded Systems"],
      specificsTag: "Slot open for new project entry",
      isEmptySlot: true,
    },
  ],

  contact: {
    title: "Get In Touch",
    subtitle:
      "I am actively looking for internship, co-op, and full-time opportunities in automation engineering, PLC programming, robotics, and mechanical design.",
    phone: "+91 79045 86593",
    email: "pranav.[email]@example.com",
    location: "Vellore / Coimbatore, Tamil Nadu, India",
    resumeUrl: "/resume.pdf",
    socials: [
      {
        platform: "LinkedIn",
        href: "#",
        icon: "Linkedin",
      },
      {
        platform: "GitHub",
        href: "#",
        icon: "Github",
      },
      {
        platform: "Email",
        href: "mailto:pranav.[email]@example.com",
        icon: "Mail",
      },
    ],
  },
};
