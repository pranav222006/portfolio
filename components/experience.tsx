"use client";

import { motion } from "framer-motion";
import { Briefcase, Calendar, MapPin, CheckCircle2, Clock } from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { portfolioContent } from "@/lib/content";

export function Experience() {
  const { experience } = portfolioContent;

  return (
    <section id="experience" className="py-20 border-b border-slate-800/80 bg-slate-950">
      <div className="mx-auto max-w-6xl px-4 sm:px-6">
        <div className="space-y-12">
          {/* Section Header */}
          <div className="space-y-2">
            <div className="flex items-center gap-2 font-mono text-xs text-sky-400 font-semibold tracking-wider">
              <span>// 03</span>
              <span>PRACTICAL INDUSTRY EXPERIENCE</span>
            </div>
            <h2 className="text-3xl font-bold tracking-tight text-slate-100 sm:text-4xl">
              Work Experience
            </h2>
          </div>

          {/* Timeline / Card List */}
          <div className="space-y-6">
            {experience.map((item) => (
              <motion.div
                key={item.id}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ duration: 0.4 }}
              >
                <Card className="border-slate-800 bg-slate-900/60 hover:border-sky-500/30 transition-all">
                  <CardHeader className="space-y-4 pb-4">
                    <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-2">
                      <div className="space-y-1">
                        <div className="flex items-center gap-2">
                          <Briefcase className="h-4 w-4 text-sky-400" />
                          <CardTitle className="text-xl font-bold text-slate-100">
                            {item.role}
                          </CardTitle>
                        </div>
                        <p className="text-base font-medium text-sky-400">
                          {item.company}
                        </p>
                      </div>

                      <div className="flex flex-wrap items-center gap-2">
                        <Badge variant="accent" className="gap-1 font-mono">
                          <Clock className="h-3 w-3" />
                          <span>{item.durationHours}</span>
                        </Badge>
                        <Badge variant="secondary" className="gap-1 font-mono">
                          <Calendar className="h-3 w-3" />
                          <span>{item.period}</span>
                        </Badge>
                      </div>
                    </div>

                    <div className="flex items-center gap-2 text-xs text-slate-400 font-mono">
                      <MapPin className="h-3.5 w-3.5 text-sky-400" />
                      <span>{item.location}</span>
                    </div>
                  </CardHeader>

                  <CardContent className="space-y-6">
                    {/* Bullet Points */}
                    <div className="space-y-3">
                      {item.bullets.map((bullet, idx) => (
                        <div key={idx} className="flex items-start gap-3">
                          <CheckCircle2 className="h-4 w-4 text-sky-400 mt-1 shrink-0" />
                          <span className="text-sm text-slate-300 leading-relaxed">
                            {bullet}
                          </span>
                        </div>
                      ))}
                    </div>

                    {/* Applied Tools Tags */}
                    <div className="pt-4 border-t border-slate-800/80">
                      <span className="text-xs font-mono text-slate-400 block mb-2 font-semibold">
                        ENGINEERING TOOLING & METHODOLOGIES:
                      </span>
                      <div className="flex flex-wrap gap-2">
                        {item.technologies.map((tech, idx) => (
                          <Badge key={idx} variant="outline" className="text-xs font-mono">
                            {tech}
                          </Badge>
                        ))}
                      </div>
                    </div>
                  </CardContent>
                </Card>
              </motion.div>
            ))}
          </div>
        </div>
      </div>
    </section>
  );
}
