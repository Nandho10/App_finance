import { Bell, User, Settings } from 'lucide-react';

export default function DashboardHeader() {
  return (
    <header className="bg-white shadow-sm border-b border-gray-200">
      <div className="container mx-auto px-4 py-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-4">
            <h1 className="text-2xl font-bold text-gray-900">App Financeiro</h1>
            <span className="text-sm text-gray-500">Dashboard</span>
          </div>
          
          <div className="flex items-center space-x-4">
            <button className="p-2 text-gray-500 hover:text-gray-700 hover:bg-gray-100 rounded-lg transition-colors">
              <Bell size={20} />
            </button>
            
            <button className="p-2 text-gray-500 hover:text-gray-700 hover:bg-gray-100 rounded-lg transition-colors">
              <Settings size={20} />
            </button>
            
            <div className="flex items-center space-x-2">
              <div className="w-8 h-8 bg-primary-600 rounded-full flex items-center justify-center">
                <User size={16} className="text-white" />
              </div>
              <span className="text-sm font-medium text-gray-700">Usuário</span>
            </div>
          </div>
        </div>
      </div>
    </header>
  );
} 