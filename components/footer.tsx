import { Cpu } from "lucide-react";

export function Footer() {
  const currentYear = new Date().getFullYear();

  return (
    <footer className="border-t border-slate-800/80 bg-slate-950 py-8 text-xs text-slate-400">
      <div className="mx-auto flex max-w-6xl flex-col items-center justify-between gap-4 px-4 sm:flex-row sm:px-6">
        <div className="flex items-center gap-2 font-mono">
          <Cpu className="h-4 w-4 text-sky-400" />
          <span>Pranav S © {currentYear}</span>
          <span className="text-slate-400">|</span>
          <span className="text-slate-400">Mechatronics Engineering Portfolio</span>
        </div>

        <div className="font-mono text-slate-400 text-center sm:text-right">
          Built with <span className="text-sky-400 font-semibold">Next.js 15</span>,{" "}
          <span className="text-sky-400 font-semibold">React 19</span> &amp;{" "}
          <span className="text-sky-400 font-semibold">Tailwind CSS</span>
        </div>
      </div>
    </footer>
  );
}
