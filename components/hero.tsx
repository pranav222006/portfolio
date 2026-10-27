"use client";

import { motion } from "framer-motion";
import { ArrowRight, Download, MapPin, Terminal, Layers } from "lucide-react";
import { Button } from "@/components/ui/button";
import { portfolioContent } from "@/lib/content";

export function Hero() {
  const { hero } = portfolioContent;

  const containerVariants = {
    hidden: { opacity: 0 },
    visible: {
      opacity: 1,
      transition: {
        staggerChildren: 0.15,
        delayChildren: 0.1,
      },
    },
  };

  const itemVariants = {
    hidden: { opacity: 0, y: 20 },
    visible: {
      opacity: 1,
      y: 0,
      transition: { duration: 0.4, ease: "easeOut" },
    },
  };

  return (
    <section className="relative overflow-hidden py-20 md:py-28 lg:py-32 border-b border-slate-800/80 bg-radial-gradient">
      {/* Engineering Grid Overlay */}
      <div className="absolute inset-0 bg-grid-pattern opacity-60 pointer-events-none" />

      <div className="relative mx-auto max-w-6xl px-4 sm:px-6">
        <motion.div
          className="flex flex-col items-start gap-6 max-w-3xl"
          variants={containerVariants}
          initial="hidden"
          animate="visible"
        >
          {/* Status Badge */}
          <motion.div variants={itemVariants} className="inline-flex items-center gap-2 rounded-full border border-sky-500/30 bg-sky-500/10 px-3.5 py-1 text-xs font-mono text-sky-400">
            <span className="relative flex h-2 w-2">
              <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-sky-400 opacity-75"></span>
              <span className="relative inline-flex rounded-full h-2 w-2 bg-sky-500"></span>
            </span>
            <span>AUTOMATION & ROBOTICS SPECIALIZATION</span>
          </motion.div>

          {/* Name & Title */}
          <motion.div variants={itemVariants} className="space-y-3">
            <h1 className="text-4xl font-extrabold tracking-tight text-slate-100 sm:text-5xl lg:text-6xl">
              {hero.name}
            </h1>
            <p className="text-xl font-medium leading-relaxed text-sky-400 sm:text-2xl">
              {hero.tagline}
            </p>
          </motion.div>

          {/* Location Subline */}
          <motion.div variants={itemVariants} className="flex items-center gap-2 text-sm text-slate-400 font-mono">
            <MapPin className="h-4 w-4 text-sky-400 shrink-0" />
            <span>{hero.subline}</span>
          </motion.div>

          {/* CTAs */}
          <motion.div variants={itemVariants} className="flex flex-wrap items-center gap-4 pt-2">
            <Button
              size="lg"
              onClick={() => {
                const el = document.getElementById("projects");
                if (el) el.scrollIntoView({ behavior: "smooth" });
              }}
              className="gap-2 group"
            >
              <span>{hero.ctaPrimary.label}</span>
              <ArrowRight className="h-4 w-4 transition-transform group-hover:translate-x-1" />
            </Button>

            <Button
              variant="outline"
              size="lg"
              onClick={() => {
                const link = document.createElement("a");
                link.href = hero.ctaSecondary.href;
                link.download = "Pranav_S_Resume.pdf";
                link.click();
              }}
              className="gap-2"
            >
              <Download className="h-4 w-4 text-sky-400" />
              <span>{hero.ctaSecondary.label}</span>
            </Button>
          </motion.div>

          {/* Engineering Metrics Quick Bar */}
          <motion.div
            variants={itemVariants}
            className="mt-8 grid grid-cols-3 gap-4 w-full pt-8 border-t border-slate-800/80"
          >
            {hero.stats.map((stat, idx) => (
              <div key={idx} className="flex flex-col space-y-1">
                <span className="font-mono text-2xl sm:text-3xl font-bold text-slate-100">
                  {stat.value}
                </span>
                <span className="text-xs text-slate-400 font-mono uppercase tracking-wider">
                  {stat.label}
                </span>
              </div>
            ))}
          </motion.div>
        </motion.div>
      </div>
    </section>
  );
}
