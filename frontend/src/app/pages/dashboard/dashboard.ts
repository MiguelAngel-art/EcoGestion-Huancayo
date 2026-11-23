
import { Component, inject, OnInit, signal } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Router } from '@angular/router';

interface ResumenDashboard {
  familias: number;
  recolecciones_completadas: number;
  total_kg: number;
  ultimas_recolecciones: unknown[];
}

@Component({
  selector: 'app-dashboard',
  standalone: true,
  imports: [],
  templateUrl: './dashboard.html',
  styleUrl: './dashboard.scss'
})
export class Dashboard implements OnInit {

  private http = inject(HttpClient);
  private router = inject(Router);

  resumen = signal<ResumenDashboard | null>(null);
  cargando = signal(true);
  error = signal('');

  ngOnInit(): void {
    this.cargarDashboard();
  }

  // Obtener estadísticas reales desde FastAPI
  cargarDashboard(): void {
    const token = sessionStorage.getItem('ecogestion_token');

    if (!token) {
      this.router.navigate(['/login']);
      return;
    }

    this.cargando.set(true);
    this.error.set('');

    const headers = new HttpHeaders({
      Authorization: `Bearer ${token}`
    });

    this.http.get<ResumenDashboard>(
      'http://127.0.0.1:8000/dashboard',
      { headers }
    ).subscribe({
      next: (datos) => {
        this.resumen.set(datos);
        this.cargando.set(false);
      },

      error: (err) => {
        this.cargando.set(false);

        if (err.status === 401) {
          sessionStorage.removeItem('ecogestion_token');
          this.router.navigate(['/login']);
        } else {
          this.error.set(
            'No se pudieron cargar las estadísticas.'
          );
        }
      }
    });
  }

  // Navegar al módulo de familias
  irFamilias(): void {
    this.router.navigate(['/familias']);
  }

  irRecolecciones(): void {
  this.router.navigate(['/recolecciones']);
  }

  irMateriales(): void {
  this.router.navigate(['/materiales']);
  }
  // Cerrar sesión
  cerrarSesion(): void {
    sessionStorage.removeItem('ecogestion_token');
    this.router.navigate(['/login']);
  }
}
