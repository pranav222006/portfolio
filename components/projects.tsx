"use client";

import { motion } from "framer-motion";
import { Bot, Navigation, Plus, Tag, ArrowUpRight, Wrench } from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { portfolioContent } from "@/lib/content";

export function Projects() {
  const { projects } = portfolioContent;

  return (
    <section id="projects" className="py-20 border-b border-slate-800/80 bg-slate-950/60">
      <div className="mx-auto max-w-6xl px-4 sm:px-6">
        <div className="space-y-12">
          {/* Section Header */}
          <div className="space-y-2">
            <div className="flex items-center gap-2 font-mono text-xs text-sky-400 font-semibold tracking-wider">
              <span>// 04</span>
              <span>TECHNICAL CASE STUDIES & BUILDS</span>
            </div>
            <h2 className="text-3xl font-bold tracking-tight text-slate-100 sm:text-4xl">
              Featured Engineering Projects
            </h2>
          </div>

          {/* Projects 2-Column Grid */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {projects.map((project) => {
              if (project.isEmptySlot) {
                return (
                  <motion.div
                    key={project.id}
                    initial={{ opacity: 0, y: 20 }}
                    whileInView={{ opacity: 1, y: 0 }}
                    viewport={{ once: true }}
                    transition={{ duration: 0.4 }}
                  >
                    <Card className="h-full border-dashed border-slate-800 bg-slate-900/20 hover:border-sky-500/40 transition-colors flex flex-col justify-center items-center p-8 text-center min-h-[320px] group">
                      <div className="flex h-12 w-12 items-center justify-center rounded-full border border-slate-800 bg-slate-900 text-slate-500 group-hover:text-sky-400 group-hover:border-sky-500/30 transition-all mb-4">
                        <Plus className="h-6 w-6" />
                      </div>
                      <CardTitle className="text-lg font-semibold text-slate-400 group-hover:text-slate-200 transition-colors mb-2">
                        {project.title}
                      </CardTitle>
                      <CardDescription className="text-xs text-slate-400 max-w-xs mb-4">
                        {project.description}
                      </CardDescription>
                      <Badge variant="secondary" className="font-mono text-[11px]">
                        + Add Project Slot Ready
                      </Badge>
                    </Card>
                  </motion.div>
                );
              }

              return (
                <motion.div
                  key={project.id}
                  initial={{ opacity: 0, y: 20 }}
                  whileInView={{ opacity: 1, y: 0 }}
                  viewport={{ once: true }}
                  transition={{ duration: 0.4 }}
                  whileHover={{ y: -4 }}
                >
                  <Card className="h-full border-slate-800 bg-slate-900/60 hover:border-sky-500/40 hover:shadow-2xl hover:shadow-sky-500/5 transition-all duration-300 flex flex-col justify-between group">
                    <CardHeader className="space-y-3 pb-4">
                      <div className="flex items-center justify-between gap-2">
                        <Badge
                          variant={project.category === "Team Project" ? "accent" : "outline"}
                          className="font-mono text-xs"
                        >
                          {project.category}
                        </Badge>
                        <span className="font-mono text-[11px] text-slate-400 flex items-center gap-1">
                          <Tag className="h-3 w-3 text-sky-400" />
                          <span>{project.specificsTag}</span>
                        </span>
                      </div>

                      <div className="space-y-1">
                        <div className="flex items-center justify-between">
                          <CardTitle className="text-xl font-bold text-slate-100 group-hover:text-sky-400 transition-colors">
                            {project.title}
                          </CardTitle>
                          <ArrowUpRight className="h-5 w-5 text-slate-500 group-hover:text-sky-400 transition-colors" />
                        </div>
                        <p className="text-xs font-mono text-slate-400">
                          {project.subtitle}
                        </p>
                      </div>

                      <p className="text-sm text-slate-300 leading-relaxed pt-1">
                        {project.description}
                      </p>
                    </CardHeader>

                    <CardContent className="space-y-4 pt-0">
                      {/* Subsystem & Key Engineering Contributions */}
                      {project.highlights && (
                        <div className="space-y-2 pt-3 border-t border-slate-800/80">
                          <span className="text-xs font-mono text-slate-400 font-semibold block flex items-center gap-1.5">
                            <Wrench className="h-3.5 w-3.5 text-sky-400" />
                            KEY TECHNICAL CONTRIBUTIONS:
                          </span>
                          <ul className="space-y-1.5 pl-4 list-disc text-xs text-slate-300">
                            {project.highlights.map((item, idx) => (
                              <li key={idx} className="leading-normal">
                                {item}
                              </li>
                            ))}
                          </ul>
                        </div>
                      )}

                      {/* Tools & Tech Badges */}
                      <div className="pt-3 border-t border-slate-800/80 flex flex-wrap gap-1.5">
                        {project.tools.map((tool, idx) => (
                          <Badge key={idx} variant="secondary" className="text-[11px] font-mono">
                            {tool}
                          </Badge>
                        ))}
                      </div>
                    </CardContent>
                  </Card>
                </motion.div>
              );
            })}
          </div>
        </div>
      </div>
    </section>
  );
}
