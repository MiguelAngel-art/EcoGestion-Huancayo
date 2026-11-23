
import { Component, inject, OnInit, signal } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Router } from '@angular/router';

interface Familia {
  id: number;
  responsable: string;
  sector: string;
}

interface Recoleccion {
  id: number;
  familia_id: number;
  fecha: string;
  estado: string;
  observacion: string;
  familia_nombre?: string;
  sector?: string;
}

@Component({
  selector: 'app-recolecciones',
  standalone: true,
  imports: [FormsModule],
  templateUrl: './recolecciones.html',
  styleUrl: './recolecciones.scss'
})
export class Recolecciones implements OnInit {

  private http = inject(HttpClient);
  private router = inject(Router);

  private apiUrl = 'http://127.0.0.1:8000';

  recolecciones = signal<Recoleccion[]>([]);
  familias = signal<Familia[]>([]);

  cargando = signal(false);
  guardando = signal(false);
  mostrarFormulario = signal(false);

  editandoId = signal<number | null>(null);
  eliminandoId = signal<number | null>(null);

  error = signal('');
  mensaje = signal('');

  formulario = {
    familia_id: 0,
    fecha: '',
    estado: 'pendiente',
    observacion: ''
  };

  ngOnInit(): void {
    this.cargarFamilias();
    this.cargarRecolecciones();
  }

  private obtenerHeaders(): HttpHeaders | null {
    const token = sessionStorage.getItem('ecogestion_token');

    if (!token) {
      this.router.navigate(['/login']);
      return null;
    }

    return new HttpHeaders({
      Authorization: `Bearer ${token}`
    });
  }

  private manejarErrorSesion(status: number): boolean {
    if (status === 401) {
      sessionStorage.removeItem('ecogestion_token');
      this.router.navigate(['/login']);
      return true;
    }

    return false;
  }

  // Obtener las familias para el formulario
  cargarFamilias(): void {
    const headers = this.obtenerHeaders();
    if (!headers) return;

    this.http.get<Familia[]>(
      `${this.apiUrl}/familias`,
      { headers }
    ).subscribe({
      next: (datos) => {
        this.familias.set(datos);
      },
      error: (err) => {
        if (!this.manejarErrorSesion(err.status)) {
          this.error.set('No se pudo cargar la lista de familias.');
        }
      }
    });
  }

  // Consultar recolecciones
  cargarRecolecciones(): void {
    const headers = this.obtenerHeaders();
    if (!headers) return;

    this.cargando.set(true);
    this.error.set('');

    this.http.get<Recoleccion[]>(
      `${this.apiUrl}/recolecciones`,
      { headers }
    ).subscribe({
      next: (datos) => {
        this.recolecciones.set(datos);
        this.cargando.set(false);
      },
      error: (err) => {
        this.cargando.set(false);

        if (!this.manejarErrorSesion(err.status)) {
          this.error.set('No se pudieron cargar las recolecciones.');
        }
      }
    });
  }

  // Abrir formulario para crear
  abrirFormulario(): void {
    this.editandoId.set(null);

    this.formulario = {
      familia_id: 0,
      fecha: '',
      estado: 'pendiente',
      observacion: ''
    };

    this.error.set('');
    this.mensaje.set('');
    this.mostrarFormulario.set(true);
  }

  // Abrir formulario para editar
  editarRecoleccion(recoleccion: Recoleccion): void {
    this.editandoId.set(recoleccion.id);

    this.formulario = {
      familia_id: recoleccion.familia_id,
      fecha: recoleccion.fecha,
      estado: recoleccion.estado,
      observacion: recoleccion.observacion ?? ''
    };

    this.error.set('');
    this.mensaje.set('');
    this.mostrarFormulario.set(true);
  }

  cancelarFormulario(): void {
    this.mostrarFormulario.set(false);
    this.editandoId.set(null);
    this.error.set('');
  }

  // Crear o actualizar recolección
  guardarRecoleccion(): void {
    const headers = this.obtenerHeaders();

    if (!headers || this.guardando()) return;

    if (!this.formulario.familia_id || !this.formulario.fecha) {
      this.error.set('Selecciona una familia y una fecha.');
      return;
    }

    const datos = {
      familia_id: Number(this.formulario.familia_id),
      fecha: this.formulario.fecha,
      estado: this.formulario.estado,
      observacion: this.formulario.observacion.trim()
    };

    const id = this.editandoId();

    this.guardando.set(true);
    this.error.set('');

    const solicitud = id !== null
      ? this.http.put<Recoleccion>(
          `${this.apiUrl}/recolecciones/${id}`,
          datos,
          { headers }
        )
      : this.http.post<Recoleccion>(
          `${this.apiUrl}/recolecciones`,
          datos,
          { headers }
        );

    solicitud.subscribe({
      next: () => {
        this.guardando.set(false);
        this.mostrarFormulario.set(false);
        this.editandoId.set(null);

        this.mensaje.set(
          id !== null
            ? 'Recolección actualizada correctamente.'
            : 'Recolección registrada correctamente.'
        );

        this.cargarRecolecciones();
      },
      error: (err) => {
        this.guardando.set(false);

        if (!this.manejarErrorSesion(err.status)) {
          this.error.set(
            'No se pudo guardar la recolección. Código: ' + err.status
          );
        }
      }
    });
  }

  // Eliminar recolección
  eliminarRecoleccion(recoleccion: Recoleccion): void {
    if (this.eliminandoId() !== null) return;

    const confirmar = window.confirm(
      `¿Deseas eliminar la recolección N.º ${recoleccion.id}?`
    );

    if (!confirmar) return;

    const headers = this.obtenerHeaders();
    if (!headers) return;

    this.eliminandoId.set(recoleccion.id);
    this.error.set('');
    this.mensaje.set('');

    this.http.delete<void>(
      `${this.apiUrl}/recolecciones/${recoleccion.id}`,
      { headers }
    ).subscribe({
      next: () => {
        this.eliminandoId.set(null);
        this.mensaje.set('Recolección eliminada correctamente.');
        this.cargarRecolecciones();
      },
      error: (err) => {
        this.eliminandoId.set(null);

        if (!this.manejarErrorSesion(err.status)) {
          this.error.set(
            'No se pudo eliminar la recolección. ' +
            'Puede tener materiales registrados. Código: ' + err.status
          );
        }
      }
    });
  }

  volverDashboard(): void {
    this.router.navigate(['/dashboard']);
  }
}
