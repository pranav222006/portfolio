"use client";

import * as React from "react";
import { motion } from "framer-motion";
import { Mail, Phone, MapPin, Download, Copy, Check, Linkedin, Github } from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { portfolioContent } from "@/lib/content";

export function Contact() {
  const { contact } = portfolioContent;
  const [copiedEmail, setCopiedEmail] = React.useState(false);
  const [copiedPhone, setCopiedPhone] = React.useState(false);

  const handleCopyEmail = () => {
    navigator.clipboard.writeText(contact.email);
    setCopiedEmail(true);
    setTimeout(() => setCopiedEmail(false), 2000);
  };

  const handleCopyPhone = () => {
    navigator.clipboard.writeText(contact.phone);
    setCopiedPhone(true);
    setTimeout(() => setCopiedPhone(false), 2000);
  };

  return (
    <section id="contact" className="py-20 border-b border-slate-800/80 bg-slate-950">
      <div className="mx-auto max-w-6xl px-4 sm:px-6">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.4 }}
          className="space-y-12"
        >
          {/* Section Header */}
          <div className="space-y-2 text-center max-w-2xl mx-auto">
            <div className="inline-flex items-center gap-2 font-mono text-xs text-sky-400 font-semibold tracking-wider">
              <span>// 05</span>
              <span>GET IN TOUCH</span>
            </div>
            <h2 className="text-3xl font-bold tracking-tight text-slate-100 sm:text-4xl">
              {contact.title}
            </h2>
            <p className="text-sm text-slate-400 leading-relaxed">
              {contact.subtitle}
            </p>
          </div>

          <div className="max-w-3xl mx-auto">
            <Card className="border-sky-500/20 bg-slate-900/60 p-6 sm:p-8">
              <CardContent className="space-y-8 p-0">
                {/* Contact Information Grid */}
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-6">
                  {/* Phone */}
                  <div className="flex items-start justify-between p-4 rounded-lg border border-slate-800 bg-slate-950/60">
                    <div className="space-y-1">
                      <div className="flex items-center gap-2 text-xs font-mono text-slate-400">
                        <Phone className="h-3.5 w-3.5 text-sky-400" />
                        <span>PHONE</span>
                      </div>
                      <p className="text-base font-semibold text-slate-100 font-mono">
                        {contact.phone}
                      </p>
                    </div>
                    <Button
                      variant="ghost"
                      size="icon"
                      onClick={handleCopyPhone}
                      className="text-slate-400 hover:text-sky-400"
                      title="Copy Phone Number"
                    >
                      {copiedPhone ? (
                        <Check className="h-4 w-4 text-emerald-400" />
                      ) : (
                        <Copy className="h-4 w-4" />
                      )}
                    </Button>
                  </div>

                  {/* Email */}
                  <div className="flex items-start justify-between p-4 rounded-lg border border-slate-800 bg-slate-950/60">
                    <div className="space-y-1">
                      <div className="flex items-center gap-2 text-xs font-mono text-slate-400">
                        <Mail className="h-3.5 w-3.5 text-sky-400" />
                        <span>EMAIL</span>
                      </div>
                      <p className="text-sm font-semibold text-slate-100 font-mono truncate max-w-[180px] sm:max-w-[200px]">
                        {contact.email}
                      </p>
                    </div>
                    <Button
                      variant="ghost"
                      size="icon"
                      onClick={handleCopyEmail}
                      className="text-slate-400 hover:text-sky-400"
                      title="Copy Email Address"
                    >
                      {copiedEmail ? (
                        <Check className="h-4 w-4 text-emerald-400" />
                      ) : (
                        <Copy className="h-4 w-4" />
                      )}
                    </Button>
                  </div>
                </div>

                {/* Location & Social Icons */}
                <div className="flex flex-col sm:flex-row items-center justify-between gap-4 pt-6 border-t border-slate-800">
                  <div className="flex items-center gap-2 text-xs text-slate-400 font-mono">
                    <MapPin className="h-4 w-4 text-sky-400" />
                    <span>{contact.location}</span>
                  </div>

                  <div className="flex items-center gap-3">
                    <a
                      href="#"
                      target="_blank"
                      rel="noopener noreferrer"
                      className="flex h-9 w-9 items-center justify-center rounded-lg border border-slate-800 bg-slate-900 text-slate-400 hover:text-sky-400 hover:border-sky-500/40 transition-colors"
                      title="LinkedIn (Add URL)"
                    >
                      <Linkedin className="h-4 w-4" />
                    </a>
                    <a
                      href="#"
                      target="_blank"
                      rel="noopener noreferrer"
                      className="flex h-9 w-9 items-center justify-center rounded-lg border border-slate-800 bg-slate-900 text-slate-400 hover:text-sky-400 hover:border-sky-500/40 transition-colors"
                      title="GitHub (Add URL)"
                    >
                      <Github className="h-4 w-4" />
                    </a>
                  </div>
                </div>

                {/* Download Resume Button */}
                <div className="pt-2">
                  <Button
                    size="lg"
                    onClick={() => {
                      const link = document.createElement("a");
                      link.href = contact.resumeUrl;
                      link.download = "Pranav_S_Resume.pdf";
                      link.click();
                    }}
                    className="w-full gap-2 font-semibold"
                  >
                    <Download className="h-4 w-4 text-slate-950" />
                    <span>Download Official Resume PDF</span>
                  </Button>
                </div>
              </CardContent>
            </Card>
          </div>
        </motion.div>
      </div>
    </section>
  );
}
