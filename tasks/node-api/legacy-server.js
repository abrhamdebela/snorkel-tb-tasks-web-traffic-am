const express = require('express');
const sqlite3 = require('sqlite3').verbose();
const path = require('path');
const fs = require('fs');

const app = express();
const PORT = process.env.PORT || 3000;

// Module-scoped singleton database connection
const DB_PATH = path.join(__dirname, 'data', 'app.db');
const db = new sqlite3.Database(DB_PATH, (err) => {
  if (err) {
    console.error('Database connection error:', err);
  } else {
    console.log('Connected to database');
    // Initialize schema
    db.serialize(() => {
      db.run(`
        CREATE TABLE IF NOT EXISTS users (
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          name TEXT NOT NULL,
          email TEXT UNIQUE NOT NULL,
          created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
      `);
    });
  }
});

// Middleware
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// Routes with inline SQL and business logic mixed together
app.get('/users', (req, res) => {
  // Inline SQL query
  db.all('SELECT * FROM users ORDER BY id', [], (err, rows) => {
    if (err) {
      res.status(500).json({ error: err.message });
    } else {
      res.status(200).json(rows);
    }
  });
});

app.get('/users/:id', (req, res) => {
  const id = parseInt(req.params.id);
  if (isNaN(id)) {
    return res.status(400).json({ error: 'Invalid user ID' });
  }
  // Inline SQL query
  db.get('SELECT * FROM users WHERE id = ?', [id], (err, row) => {
    if (err) {
      res.status(500).json({ error: err.message });
    } else if (!row) {
      res.status(404).json({ error: 'User not found' });
    } else {
      res.status(200).json(row);
    }
  });
});

app.post('/users', (req, res) => {
  const { name, email } = req.body;
  if (!name || !email) {
    return res.status(400).json({ error: 'Name and email are required' });
  }
  // Inline SQL with business logic
  db.run('INSERT INTO users (name, email) VALUES (?, ?)', [name, email], function(err) {
    if (err) {
      if (err.message.includes('UNIQUE constraint')) {
        res.status(400).json({ error: 'Email already exists' });
      } else {
        res.status(500).json({ error: err.message });
      }
    } else {
      // Fetch the created user
      db.get('SELECT * FROM users WHERE id = ?', [this.lastID], (getErr, row) => {
        if (getErr) {
          res.status(500).json({ error: getErr.message });
        } else {
          res.status(201).json(row);
        }
      });
    }
  });
});

app.put('/users/:id', (req, res) => {
  const id = parseInt(req.params.id);
  if (isNaN(id)) {
    return res.status(400).json({ error: 'Invalid user ID' });
  }
  const { name, email } = req.body;
  const updates = [];
  const values = [];
  if (name !== undefined) {
    updates.push('name = ?');
    values.push(name);
  }
  if (email !== undefined) {
    updates.push('email = ?');
    values.push(email);
  }
  if (updates.length === 0) {
    db.get('SELECT * FROM users WHERE id = ?', [id], (err, row) => {
      if (err) {
        res.status(500).json({ error: err.message });
      } else if (!row) {
        res.status(404).json({ error: 'User not found' });
      } else {
        res.status(200).json(row);
      }
    });
    return;
  }
  values.push(id);
  // Inline SQL update
  db.run(`UPDATE users SET ${updates.join(', ')} WHERE id = ?`, values, function(err) {
    if (err) {
      res.status(500).json({ error: err.message });
    } else if (this.changes === 0) {
      res.status(404).json({ error: 'User not found' });
    } else {
      db.get('SELECT * FROM users WHERE id = ?', [id], (getErr, row) => {
        if (getErr) {
          res.status(500).json({ error: getErr.message });
        } else {
          res.status(200).json(row);
        }
      });
    }
  });
});

app.delete('/users/:id', (req, res) => {
  const id = parseInt(req.params.id);
  if (isNaN(id)) {
    return res.status(400).json({ error: 'Invalid user ID' });
  }
  // Inline SQL delete
  db.run('DELETE FROM users WHERE id = ?', [id], function(err) {
    if (err) {
      res.status(500).json({ error: err.message });
    } else if (this.changes === 0) {
      res.status(404).json({ error: 'User not found' });
    } else {
      res.status(200).json({ message: 'User deleted successfully' });
    }
  });
});

// Health check endpoint
app.get('/health', (req, res) => {
  res.status(200).json({ status: 'ok' });
});

// Error handling middleware
app.use((err, req, res, next) => {
  const statusCode = err.statusCode || 500;
  const message = err.message || 'Internal Server Error';
  res.status(statusCode).json({ error: message });
});

// Start server
app.listen(PORT, () => {
  console.log(`Server is running on port ${PORT}`);
});

