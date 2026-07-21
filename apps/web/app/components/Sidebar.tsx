type SidebarProps = {
  alertCount: number;
};

const navigation = [
  { href: "#overview", icon: "◒", label: "Обзор" },
  { href: "#margins", icon: "⌁", label: "Юнит-экономика" },
  { href: "#alerts", icon: "◇", label: "Сигналы" },
  { href: "#cost", icon: "↗", label: "Себестоимость" },
];

export function Sidebar({ alertCount }: SidebarProps) {
  return (
    <aside className="sidebar">
      <a className="brand" href="#overview" aria-label="margin-guard — на главную">
        <span className="brand-symbol"><i /><i /></span>
        <span>margin<span>guard</span></span>
      </a>

      <div className="nav-caption">Пространство</div>
      <nav aria-label="Основная навигация">
        {navigation.map((item, index) => (
          <a className={`nav-link ${index === 0 ? "active" : ""}`} href={item.href} key={item.href}>
            <span className="nav-icon">{item.icon}</span>
            <span>{item.label}</span>
            {item.href === "#alerts" && <b>{alertCount}</b>}
          </a>
        ))}
      </nav>

      <div className="sidebar-insight">
        <span className="insight-orbit"><i /></span>
        <p>Здоровье портфеля</p>
        <strong>87%</strong>
        <small>Отличная динамика</small>
      </div>

      <div className="sidebar-footer">
        <span className="live-dot" />
        <div><b>Live sync</b><small>обновлено сейчас</small></div>
        <button aria-label="Настройки">•••</button>
      </div>
    </aside>
  );
}
