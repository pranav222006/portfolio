import * as React from "react";
import { cn } from "@/lib/utils";

export interface BadgeProps extends React.HTMLAttributes<HTMLDivElement> {
  variant?: "default" | "secondary" | "accent" | "outline";
}

function Badge({ className, variant = "default", ...props }: BadgeProps) {
  const baseStyles =
    "inline-flex items-center rounded-md border px-2.5 py-0.5 text-xs font-mono font-medium transition-colors focus:outline-none focus:ring-2 focus:ring-sky-400 focus:ring-offset-2";

  const variants = {
    default:
      "border-transparent bg-slate-800 text-slate-200 hover:bg-slate-700",
    secondary:
      "border-slate-800 bg-slate-900 text-slate-400 font-normal",
    accent:
      "border-sky-500/30 bg-sky-500/10 text-sky-400 hover:bg-sky-500/20",
    outline:
      "border-slate-700 text-slate-300 hover:border-slate-600",
  };

  return (
    <div
      className={cn(baseStyles, variants[variant], className)}
      {...props}
    />
  );
}

export { Badge };
