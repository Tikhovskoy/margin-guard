import Image from "next/image";

type DataMode = "loading" | "live" | "mock" | "demo" | "error";

type SidebarProps = {
  alertCount: number;
  dataMode: DataMode;
};

const navigation = [
  {
    href: "#overview",
    label: "Обзор",
    icon: <path d="M4 13h6V4H4v9Zm0 7h6v-3H4v3Zm10 0h6V11h-6v9Zm0-13h6V4h-6v3Z" />,
  },
  {
    href: "#risks",
    label: "Риски",
    icon: <><path d="M12 3 2.8 19h18.4L12 3Z" /><path d="M12 9v4m0 3h.01" /></>,
  },
  {
    href: "#products",
    label: "Все товары",
    icon: <path d="M4 5h16M4 12h16M4 19h16" />,
  },
];

const connectionCopy: Record<DataMode, { title: string; detail: string }> = {
  loading: { title: "Подключение", detail: "Получаем preview" },
  live: { title: "Реальные данные", detail: "Live API" },
  mock: { title: "Демонстрация", detail: "Mock API" },
  demo: { title: "Демонстрация", detail: "Локальный набор" },
  error: { title: "Ошибка данных", detail: "Проверьте подключение" },
};

export function Sidebar({ alertCount, dataMode }: SidebarProps) {
  const connection = connectionCopy[dataMode];

  return (
    <aside className="sidebar">
      <a className="brand" href="#overview" aria-label="Margin Guard — к обзору">
        <Image className="brand-logo" src="/brand/margin-guard-logo-v2.svg" alt="Margin Guard" width={160} height={33} priority />
        <Image className="brand-mark" src="/brand/margin-guard-mark-v2.svg" alt="" width={28} height={28} />
      </a>

      <p className="nav-label">Рабочая область</p>
      <nav className="side-nav" aria-label="Основная навигация">
        {navigation.map((item, index) => (
          <a className={index === 0 ? "active" : ""} href={item.href} key={item.href}>
            <svg viewBox="0 0 24 24" aria-hidden="true">{item.icon}</svg>
            <span>{item.label}</span>
            {item.href === "#risks" && <b className="nav-count">{alertCount}</b>}
          </a>
        ))}
      </nav>

      <div className={`sync sync-${dataMode}`} role="status">
        <div className="sync-line"><i className="sync-dot" /><b>{connection.title}</b></div>
        <small>{connection.detail}</small>
      </div>
    </aside>
  );
}
