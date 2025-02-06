// Importar módulos necesarios
const express = require('express');
const mysql = require('mysql');
const cors = require('cors');
const helmet = require('helmet'); // Seguridad adicional

const app = express();

// Deshabilitar la cabecera "X-Powered-By" para ocultar la versión de Express
app.disable('x-powered-by');

// Usar Helmet para añadir seguridad extra (cabezaras HTTP seguras)
app.use(helmet());

// Configuración de CORS con restricciones
const corsOptions = {
  origin: ['https://tu-dominio.com', 'https://otro-dominio.com'], // Dominios permitidos
  methods: ['GET', 'POST', 'PUT', 'DELETE'],
  allowedHeaders: ['Content-Type', 'Authorization'],
  credentials: true
};

// Habilitar CORS con las opciones definidas
app.use(cors(corsOptions));

// Middleware para parsear JSON en las peticiones
app.use(express.json());

// Configuración segura de la conexión a MySQL con un pool de conexiones
const pool = mysql.createPool({
  connectionLimit: 10, // Limitar el número de conexiones abiertas
  host: process.env.DB_HOST || 'db',
  user: process.env.DB_USER || 'root',
  password: process.env.DB_PASSWORD || '',
  database: process.env.DB_DATABASE || 'bd-taller'
});

// Función para ejecutar consultas SQL de forma segura
const executeQuery = (sql, values, res) => {
  pool.query(sql, values, (err, results) => {
    if (err) return res.status(500).json({ error: err.message });
    res.json(results);
  });
};

// --------------------------- 
// Endpoints para USUARIOS y ROLES
// --------------------------- 

app.get('/users', (req, res) => {
  executeQuery("SELECT * FROM users", [], res);
});

app.get('/users/:id', (req, res) => {
  executeQuery("SELECT * FROM users WHERE id = ?", [req.params.id], res);
});

app.post('/users', (req, res) => {
  const { username, role } = req.body;
  if (!username || !role) return res.status(400).json({ error: 'Faltan datos' });
  executeQuery("INSERT INTO users (username, role) VALUES (?, ?)", [username, role], res);
});

app.put('/users', (req, res) => {
  const { id, username, role } = req.body;
  if (!id || !username || !role) return res.status(400).json({ error: 'Faltan datos' });
  executeQuery("UPDATE users SET username = ?, role = ? WHERE id = ?", [username, role, id], res);
});

app.delete('/users', (req, res) => {
  const { id } = req.body;
  if (!id) return res.status(400).json({ error: 'Faltan datos' });
  executeQuery("DELETE FROM users WHERE id = ?", [id], res);
});

// Manejo de errores para rutas no definidas
app.use((req, res) => {
  res.status(404).json({ error: 'Ruta no encontrada' });
});

// Manejo global de errores
app.use((err, req, res, next) => {
  console.error(err.stack);
  res.status(500).json({ error: 'Error interno del servidor' });
});

// Iniciar el servidor en el puerto 3000 o el definido en PORT
const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`Servidor corriendo en http://localhost:${PORT}`);
});
