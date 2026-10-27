import * as React from "react";
import { cn } from "@/lib/utils";

export interface ButtonProps
  extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: "default" | "outline" | "ghost" | "secondary" | "accent";
  size?: "default" | "sm" | "lg" | "icon";
  asChild?: boolean;
}

const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(
  ({ className, variant = "default", size = "default", ...props }, ref) => {
    const baseStyles =
      "inline-flex items-center justify-center whitespace-nowrap rounded-md text-sm font-medium transition-all focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-sky-400 focus-visible:ring-offset-2 focus-visible:ring-offset-slate-950 disabled:pointer-events-none disabled:opacity-50 active:scale-[0.98]";

    const variants = {
      default:
        "bg-sky-500 text-slate-950 hover:bg-sky-400 font-semibold shadow-lg shadow-sky-500/20",
      accent:
        "bg-sky-500/10 text-sky-400 border border-sky-500/30 hover:bg-sky-500/20 hover:border-sky-400 font-medium",
      outline:
        "border border-slate-800 bg-slate-900/60 text-slate-200 hover:bg-slate-800 hover:text-white hover:border-slate-700",
      secondary:
        "bg-slate-800 text-slate-200 hover:bg-slate-700 hover:text-white",
      ghost:
        "text-slate-400 hover:bg-slate-800/60 hover:text-slate-100",
    };

    const sizes = {
      default: "h-10 px-4 py-2",
      sm: "h-8 rounded-md px-3 text-xs",
      lg: "h-11 rounded-md px-6 text-base",
      icon: "h-9 w-9 p-0",
    };

    return (
      <button
        className={cn(baseStyles, variants[variant], sizes[size], className)}
        ref={ref}
        {...props}
      />
    );
  }
);
Button.displayName = "Button";

export { Button };
