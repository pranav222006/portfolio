"use client";

import { motion } from "framer-motion";
import { GraduationCap, CheckCircle2, Award, BookOpen } from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { portfolioContent } from "@/lib/content";

export function About() {
  const { about } = portfolioContent;

  return (
    <section id="about" className="py-20 border-b border-slate-800/80 bg-slate-950">
      <div className="mx-auto max-w-6xl px-4 sm:px-6">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.4 }}
          className="space-y-12"
        >
          {/* Section Header */}
          <div className="space-y-2">
            <div className="flex items-center gap-2 font-mono text-xs text-sky-400 font-semibold tracking-wider">
              <span>// 01</span>
              <span>ENGINEERING PROFILE</span>
            </div>
            <h2 className="text-3xl font-bold tracking-tight text-slate-100 sm:text-4xl">
              {about.title}
            </h2>
          </div>

          <div className="grid grid-cols-1 gap-8 lg:grid-cols-12">
            {/* Bio Summary */}
            <div className="lg:col-span-7 space-y-6">
              <p className="text-base leading-relaxed text-slate-300 sm:text-lg">
                {about.summary}
              </p>

              {/* Core Competency Bullets */}
              <div className="space-y-3 pt-4">
                <h3 className="text-sm font-mono text-slate-400 font-semibold uppercase tracking-wider">
                  Technical Core Focus Areas
                </h3>
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                  {about.keyHighlights.map((highlight, idx) => (
                    <div
                      key={idx}
                      className="flex items-start gap-2.5 rounded-lg border border-slate-800/80 bg-slate-900/40 p-3"
                    >
                      <CheckCircle2 className="h-4 w-4 text-sky-400 mt-0.5 shrink-0" />
                      <span className="text-xs font-medium text-slate-200">
                        {highlight}
                      </span>
                    </div>
                  ))}
                </div>
              </div>
            </div>

            {/* Education Card */}
            <div className="lg:col-span-5">
              <Card className="border-sky-500/20 bg-slate-900/60 relative overflow-hidden">
                <div className="absolute top-0 right-0 p-4 opacity-10">
                  <GraduationCap className="h-24 w-24 text-sky-400" />
                </div>
                <CardHeader className="space-y-1 pb-4">
                  <div className="flex items-center gap-2 text-xs font-mono text-sky-400">
                    <BookOpen className="h-4 w-4" />
                    <span>ACADEMIC BACKGROUND</span>
                  </div>
                  <CardTitle className="text-xl font-bold text-slate-100">
                    {about.education.degree}
                  </CardTitle>
                  <p className="text-sm font-medium text-sky-400">
                    {about.education.field}
                  </p>
                </CardHeader>

                <CardContent className="space-y-4">
                  <div className="space-y-1">
                    <p className="text-base font-semibold text-slate-200">
                      {about.education.institution}
                    </p>
                    <p className="text-xs text-slate-400 font-mono">
                      {about.education.location}
                    </p>
                  </div>

                  <div className="flex flex-wrap items-center justify-between gap-2 pt-2 border-t border-slate-800/80">
                    <Badge variant="accent">{about.education.expectedGraduation}</Badge>
                    <Badge variant="secondary">{about.education.status}</Badge>
                  </div>
                </CardContent>
              </Card>
            </div>
          </div>
        </motion.div>
      </div>
    </section>
  );
}
