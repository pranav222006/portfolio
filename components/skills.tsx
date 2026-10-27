"use client";

import { motion } from "framer-motion";
import { Compass, Cpu, Zap, Hammer } from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { portfolioContent } from "@/lib/content";

const iconMap = {
  Compass: Compass,
  Cpu: Cpu,
  Zap: Zap,
  Hammer: Hammer,
};

export function Skills() {
  const { skills } = portfolioContent;

  const containerVariants = {
    hidden: { opacity: 0 },
    visible: {
      opacity: 1,
      transition: {
        staggerChildren: 0.1,
      },
    },
  };

  const cardVariants = {
    hidden: { opacity: 0, y: 20 },
    visible: {
      opacity: 1,
      y: 0,
      transition: { duration: 0.4 },
    },
  };

  return (
    <section id="skills" className="py-20 border-b border-slate-800/80 bg-slate-950/60 relative">
      <div className="mx-auto max-w-6xl px-4 sm:px-6">
        <div className="space-y-12">
          {/* Section Header */}
          <div className="space-y-2">
            <div className="flex items-center gap-2 font-mono text-xs text-sky-400 font-semibold tracking-wider">
              <span>// 02</span>
              <span>TECHNICAL CAPABILITIES</span>
            </div>
            <h2 className="text-3xl font-bold tracking-tight text-slate-100 sm:text-4xl">
              Skills & Tooling
            </h2>
          </div>

          {/* 4-Category Grid */}
          <motion.div
            variants={containerVariants}
            initial="hidden"
            whileInView="visible"
            viewport={{ once: true }}
            className="grid grid-cols-1 md:grid-cols-2 gap-6"
          >
            {skills.map((category) => {
              const IconComponent = iconMap[category.iconName as keyof typeof iconMap] || Cpu;

              return (
                <motion.div key={category.id} variants={cardVariants}>
                  <Card className="h-full border-slate-800 bg-slate-900/50 hover:border-sky-500/40 transition-colors group">
                    <CardHeader className="space-y-3 pb-4">
                      <div className="flex items-center gap-3">
                        <div className="flex h-10 w-10 items-center justify-center rounded-lg border border-sky-500/30 bg-sky-500/10 text-sky-400 group-hover:bg-sky-500/20 group-hover:border-sky-400 transition-all">
                          <IconComponent className="h-5 w-5" />
                        </div>
                        <div>
                          <CardTitle className="text-lg font-bold text-slate-100 group-hover:text-sky-400 transition-colors">
                            {category.category}
                          </CardTitle>
                          <CardDescription className="text-xs text-slate-400 mt-0.5">
                            {category.description}
                          </CardDescription>
                        </div>
                      </div>
                    </CardHeader>

                    <CardContent>
                      <div className="flex flex-wrap gap-2 pt-2 border-t border-slate-800/60">
                        {category.skills.map((skill, idx) => (
                          <Badge
                            key={idx}
                            variant="accent"
                            className="text-xs px-3 py-1 font-mono tracking-wide"
                          >
                            {skill}
                          </Badge>
                        ))}
                      </div>
                    </CardContent>
                  </Card>
                </motion.div>
              );
            })}
          </motion.div>
        </div>
      </div>
    </section>
  );
}
