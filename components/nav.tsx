"use client";

import * as React from "react";
import { Menu, Cpu } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Sheet } from "@/components/ui/sheet";

const navLinks = [
  { label: "About", href: "#about" },
  { label: "Skills", href: "#skills" },
  { label: "Experience", href: "#experience" },
  { label: "Projects", href: "#projects" },
  { label: "Contact", href: "#contact" },
];

export function Nav() {
  const [isOpen, setIsOpen] = React.useState(false);
  const [activeSection, setActiveSection] = React.useState("");

  React.useEffect(() => {
    const handleScroll = () => {
      const sections = navLinks.map((link) => link.href.substring(1));
      const scrollPosition = window.scrollY + 100;

      for (const section of sections) {
        const el = document.getElementById(section);
        if (el) {
          const top = el.offsetTop;
          const height = el.offsetHeight;
          if (scrollPosition >= top && scrollPosition < top + height) {
            setActiveSection(section);
            break;
          }
        }
      }
    };

    window.addEventListener("scroll", handleScroll);
    return () => window.removeEventListener("scroll", handleScroll);
  }, []);

  return (
    <header className="sticky top-0 z-40 w-full border-b border-slate-800/80 bg-slate-950/80 backdrop-blur-md">
      <div className="mx-auto flex max-w-6xl items-center justify-between px-4 py-3.5 sm:px-6">
        {/* Brand Logo / Name */}
        <a
          href="#"
          className="group flex items-center gap-2.5 text-base font-semibold text-slate-100 transition-colors hover:text-sky-400"
        >
          <div className="flex h-8 w-8 items-center justify-center rounded-lg border border-sky-500/30 bg-sky-500/10 text-sky-400 group-hover:bg-sky-500/20 group-hover:border-sky-400 transition-all">
            <Cpu className="h-4 w-4" />
          </div>
          <div className="flex flex-col">
            <span className="leading-tight font-bold">Pranav S</span>
            <span className="font-mono text-[10px] tracking-wider text-slate-400 font-normal">
              MECHATRONICS
            </span>
          </div>
        </a>

        {/* Desktop Nav */}
        <nav className="hidden items-center gap-1 md:flex">
          {navLinks.map((link) => {
            const sectionId = link.href.substring(1);
            const isActive = activeSection === sectionId;
            return (
              <a
                key={link.label}
                href={link.href}
                className={`px-3 py-1.5 text-sm font-medium transition-all rounded-md ${
                  isActive
                    ? "text-sky-400 bg-sky-500/10 border border-sky-500/20"
                    : "text-slate-300 hover:text-white hover:bg-slate-900"
                }`}
              >
                {link.label}
              </a>
            );
          })}
          <div className="ml-2 pl-2 border-l border-slate-800">
            <Button
              variant="accent"
              size="sm"
              onClick={() => {
                const link = document.createElement("a");
                link.href = "/resume.pdf";
                link.download = "Pranav_S_Resume.pdf";
                link.click();
              }}
            >
              Resume PDF
            </Button>
          </div>
        </nav>

        {/* Mobile Hamburger Button */}
        <div className="flex md:hidden">
          <Button
            variant="ghost"
            size="icon"
            onClick={() => setIsOpen(true)}
            aria-label="Open Navigation Menu"
          >
            <Menu className="h-5 w-5 text-slate-300" />
          </Button>
        </div>
      </div>

      {/* Mobile Drawer Sheet */}
      <Sheet isOpen={isOpen} onClose={() => setIsOpen(false)}>
        <div className="flex flex-col gap-4 pt-2">
          {navLinks.map((link) => (
            <a
              key={link.label}
              href={link.href}
              onClick={() => setIsOpen(false)}
              className="flex items-center justify-between rounded-lg px-3 py-2.5 text-base font-medium text-slate-200 hover:bg-slate-900 hover:text-sky-400 transition-colors"
            >
              <span>{link.label}</span>
              <span className="font-mono text-xs text-slate-400">→</span>
            </a>
          ))}
          <div className="pt-4 border-t border-slate-800 mt-2">
            <a
              href="/resume.pdf"
              target="_blank"
              rel="noopener noreferrer"
              className="w-full flex items-center justify-center gap-2 rounded-lg bg-sky-500 px-4 py-2.5 text-sm font-semibold text-slate-950 hover:bg-sky-400 transition-colors"
            >
              Download Resume PDF
            </a>
          </div>
        </div>
      </Sheet>
    </header>
  );
}
