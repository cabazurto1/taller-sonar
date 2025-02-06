import React, { useEffect, useState } from 'react';

// Definimos la interfaz para el producto
interface Product {
  id: string;
  nombre: string;
  descripcion: string;
  precio: string;
  categoria_id: string;
  categoria_nombre: string;
}

const PhpApiPage: React.FC = () => {
  // Estado para almacenar la lista de productos
  const [products, setProducts] = useState<Product[]>([]);

  useEffect(() => {
    // Realiza la petición a la API REST de productos de PHP
    fetch('http://localhost:8080/proyecto/public/productos')
      .then((res) => res.json())
      .then((data: Product[]) => setProducts(data))
      .catch((err) => console.error("Error fetching products:", err));
  }, []);

  return (
    <div>
      <h2>Productos (API PHP)</h2>
      <table style={{ width: '100%', borderCollapse: 'collapse' }}>
        <thead>
          <tr>
            <th style={{ border: '1px solid #ccc', padding: '8px' }}>ID</th>
            <th style={{ border: '1px solid #ccc', padding: '8px' }}>Nombre</th>
            <th style={{ border: '1px solid #ccc', padding: '8px' }}>Descripción</th>
            <th style={{ border: '1px solid #ccc', padding: '8px' }}>Precio</th>
            <th style={{ border: '1px solid #ccc', padding: '8px' }}>Categoría</th>
          </tr>
        </thead>
        <tbody>
          {products.map((product) => (
            <tr key={product.id}>
              <td style={{ border: '1px solid #ccc', padding: '8px' }}>{product.id}</td>
              <td style={{ border: '1px solid #ccc', padding: '8px' }}>{product.nombre}</td>
              <td style={{ border: '1px solid #ccc', padding: '8px' }}>{product.descripcion}</td>
              <td style={{ border: '1px solid #ccc', padding: '8px' }}>{product.precio}</td>
              <td style={{ border: '1px solid #ccc', padding: '8px' }}>{product.categoria_nombre}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default PhpApiPage;
