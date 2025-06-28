'use client';
import { useState } from 'react';
import { FaChartPie, FaMoneyBillWave, FaWallet, FaListAlt, FaCog, FaChevronLeft, FaChevronRight, FaUserCircle } from 'react-icons/fa';
import Link from 'next/link';

const menuItems = [
  { label: 'Dashboard', icon: <FaChartPie />, href: '/' },
  { label: 'Receitas', icon: <FaMoneyBillWave />, href: '/incomes' },
  { label: 'Despesas', icon: <FaWallet />, href: '/expenses' },
  { label: 'Orçamentos', icon: <FaListAlt />, href: '/budgets' },
  { label: 'Relatórios', icon: <FaChartPie />, href: '/reports' },
  { label: 'Configurações', icon: <FaCog />, href: '/settings' },
];

export default function Sidebar() {
  // Simulação de usuário logado
  const user = { name: 'Usuário', avatar: null };

  return (
    <aside
      className="h-screen bg-white border-r border-gray-200 flex flex-col transition-all duration-200 w-56 min-w-[14rem] max-w-[14rem]"
    >
      {/* Botão de colapso REMOVIDO */}
      <div className="flex items-center h-16 px-2 border-b border-gray-100 justify-between min-w-0">
        <span className="font-bold text-lg text-gray-700 transition-all duration-200 select-none flex-1 min-w-0" style={{ minWidth: 80, display: 'inline-block' }}>
          Financeiro
        </span>
        {/* Botão removido aqui */}
      </div>
      {/* Menu */}
      <nav className="flex-1 py-4 flex flex-col gap-1">
        {menuItems.map(item => (
          <Link href={item.href} key={item.label} legacyBehavior>
            <a className="flex items-center gap-3 px-4 py-2 rounded-md text-gray-700 hover:bg-gray-100 transition-colors group">
              <span className="text-xl">{item.icon}</span>
              <span className="transition-all duration-200">{item.label}</span>
            </a>
          </Link>
        ))}
      </nav>
      {/* Rodapé com usuário */}
      <div className="flex items-center gap-3 px-4 py-4 border-t border-gray-100">
        <span className="text-2xl text-gray-400"><FaUserCircle /></span>
        <span className="text-gray-700 font-medium transition-all duration-200">{user.name}</span>
      </div>
    </aside>
  );
} 