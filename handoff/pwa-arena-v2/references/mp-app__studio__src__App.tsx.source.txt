import { AnimatePresence, motion, useReducedMotion } from "framer-motion";
import { ToastViewport } from "./components/Feedback";
import { UpdateBanner } from "./components/UpdateBanner";
import { Sidebar } from "./components/Sidebar";
import { TopBar } from "./components/TopBar";
import { CheckIn } from "./pages/CheckIn";
import { Finance } from "./pages/Finance";
import { Expenses } from "./pages/Expenses";
import { Analytics } from "./pages/Analytics";
import { Dashboard } from "./pages/Dashboard";
import { Members } from "./pages/Members";
import { Assessment } from "./pages/Assessment";
import { Chat } from "./pages/Chat";
import { Nutrition } from "./pages/Nutrition";
import { Programs } from "./pages/Programs";
import { Settings } from "./pages/Settings";
import { Shop } from "./pages/Shop";
import { useAppStore } from "./stores/appStore";
import { AuthProvider, useAuth } from "./auth/AuthContext";
import { Login } from "./pages/Login";
import { canSeePage, parseRole } from "./lib/roleNav";

const pages = {
  dashboard: Dashboard,
  members: Members,
  programs: Programs,
  nutrition: Nutrition,
  assessment: Assessment,
  chat: Chat,
  checkin: CheckIn,
  finance: Finance,
  expenses: Expenses,
  analytics: Analytics,
  settings: Settings,
  shop: Shop,
} as const;

/** گیت نشست؛ هیچ صفحهٔ محافظت‌شده‌ای پیش از اعتبارسنجی session نمایش داده نمی‌شود. */
function AppContent() {
  const { status } = useAuth();
  const page = useAppStore((s) => s.page);
  const Page = pages[page];
  const role = parseRole();
  const pageAllowed = role !== null && canSeePage(page, role);
  const reduced = useReducedMotion(); // احترام به prefers-reduced-motion (M07)

  if (status === "checking") {
    return <main role="status" className="flex min-h-screen items-center justify-center text-ink-dim">در حال بررسی نشست…</main>;
  }
  if (status === "unauthenticated") return <Login />;

  return (
    <div className="flex min-h-screen gap-6 p-6">
      <Sidebar />
      <main className="min-w-0 flex-1">
        <TopBar />
        <AnimatePresence mode="wait">
          <motion.div
            key={page}
            initial={reduced ? false : { opacity: 0, y: 14 }}
            animate={{ opacity: 1, y: 0 }}
            exit={reduced ? undefined : { opacity: 0, y: -10 }}
            transition={{ duration: reduced ? 0 : 0.3, ease: "easeOut" }}
          >
            {pageAllowed ? (
              <Page />
            ) : (
              <div className="glass-card p-5 text-sm text-ink-dim" role="alert">
                دسترسی به این صفحه برای نقش جاری مجاز نیست.
              </div>
            )}
          </motion.div>
        </AnimatePresence>
        <UpdateBanner current={__APP_VERSION__} />
        <ToastViewport />
        <footer className="mt-10 pb-2 text-center text-xs text-ink-dim">
          Muscle Paradise — سیستم‌عامل باشگاه · ساخته‌شده با عشق به جزئیات 💚
        </footer>
      </main>
    </div>
  );
}

export default function App() {
  return (
    <AuthProvider>
      <AppContent />
    </AuthProvider>
  );
}
