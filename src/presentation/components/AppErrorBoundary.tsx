import { Component, type ErrorInfo, type ReactNode } from "react";

interface Props { children: ReactNode }
interface State { error: Error | null }

export class AppErrorBoundary extends Component<Props, State> {
  state: State = { error: null };

  static getDerivedStateFromError(error: Error): State {
    return { error };
  }

  componentDidCatch(error: Error, info: ErrorInfo) {
    console.error("DispatchAI render error", error, info);
  }

  render() {
    if (this.state.error) return <main className="app-crash-screen"><div><span>REACT RENDER ERROR</span><h1>The screen could not render.</h1><p>{this.state.error.message || "Unknown application error"}</p><button type="button" onClick={() => window.location.reload()}>Reload app</button></div></main>;
    return this.props.children;
  }
}
