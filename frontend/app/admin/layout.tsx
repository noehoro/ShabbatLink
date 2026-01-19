'use client';

import React, { useEffect, useState } from 'react';
import { useRouter, usePathname } from 'next/navigation';
import Link from 'next/link';
import { getAdminToken, clearAdminToken } from '../../lib/api';
import { Spinner } from '../../components/ui';
import styles from './layout.module.css';

export default function AdminLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const router = useRouter();
  const pathname = usePathname();
  const [isAuthenticated, setIsAuthenticated] = useState<boolean | null>(null);

  // Don't apply layout to login page
  const isLoginPage = pathname === '/admin';

  useEffect(() => {
    const token = getAdminToken();
    if (!token && !isLoginPage) {
      router.push('/admin');
    } else {
      setIsAuthenticated(!!token);
    }
  }, [pathname, router, isLoginPage]);

  const handleLogout = () => {
    clearAdminToken();
    router.push('/admin');
  };

  // Login page doesn't use the admin layout
  if (isLoginPage) {
    return <>{children}</>;
  }

  // Loading state
  if (isAuthenticated === null) {
    return (
      <div className={styles.loading}>
        <Spinner size="lg" />
      </div>
    );
  }

  // Not authenticated
  if (!isAuthenticated) {
    return null;
  }

  const navItems = [
    { href: '/admin/dashboard', label: 'Dashboard', icon: '📊' },
    { href: '/admin/guests', label: 'Guests', icon: '👥' },
    { href: '/admin/hosts', label: 'Hosts', icon: '🏠' },
    { href: '/admin/matches', label: 'Matches', icon: '🔗' },
  ];

  return (
    <div className={styles.layout}>
      {/* Sidebar */}
      <aside className={styles.sidebar}>
        <div className={styles.logo}>
          <span className={styles.logoIcon}>✡</span>
          <span className={styles.logoText}>ShabbatLink</span>
        </div>
        
        <nav className={styles.nav}>
          {navItems.map((item) => (
            <Link
              key={item.href}
              href={item.href}
              className={`${styles.navItem} ${pathname === item.href ? styles.active : ''}`}
            >
              <span className={styles.navIcon}>{item.icon}</span>
              <span>{item.label}</span>
            </Link>
          ))}
        </nav>

        <div className={styles.sidebarFooter}>
          <button onClick={handleLogout} className={styles.logoutBtn}>
            Logout
          </button>
        </div>
      </aside>

      {/* Main Content */}
      <main className={styles.main}>
        {children}
      </main>
    </div>
  );
}
