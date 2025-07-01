// Teste simples para verificar se a API está acessível via frontend
const testAPI = async () => {
  try {
    console.log('Testando API via frontend...');
    
    // Teste 1: API direta do Django
    const djangoResponse = await fetch('http://localhost:8000/api/sales-kpis/');
    console.log('✅ Django API:', djangoResponse.status);
    
    if (djangoResponse.ok) {
      const djangoData = await djangoResponse.json();
      console.log('Dados Django:', djangoData);
    }
    
    // Teste 2: API via proxy do Next.js
    const nextResponse = await fetch('http://localhost:3000/api/sales-kpis/');
    console.log('✅ Next.js Proxy:', nextResponse.status);
    
    if (nextResponse.ok) {
      const nextData = await nextResponse.json();
      console.log('Dados Next.js:', nextData);
    } else {
      console.log('❌ Erro Next.js:', nextResponse.status, nextResponse.statusText);
    }
    
  } catch (error) {
    console.error('❌ Erro no teste:', error.message);
  }
};

// Executar teste
testAPI(); 