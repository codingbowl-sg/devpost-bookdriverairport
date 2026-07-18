import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import { App } from "./presentation/App";
import { AppErrorBoundary } from "./presentation/components/AppErrorBoundary";
import "./styles.css";
import "./mode.css";

createRoot(document.getElementById("root")!).render(<StrictMode><AppErrorBoundary><App /></AppErrorBoundary></StrictMode>);
