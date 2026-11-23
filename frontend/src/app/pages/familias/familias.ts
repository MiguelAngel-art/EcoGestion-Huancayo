
import { Component, inject, OnInit, signal } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Router } from '@angular/router';

interface Familia {
  id: number;
  responsable: string;
  sector: string;
  direccion: string;
  telefono: string | null;
}

@Component({
  selector: 'app-familias',
  standalone: true,
  imports: [FormsModule],
  templateUrl: './familias.html',
  styleUrl: './familias.scss'
})
export class Familias implements OnInit {

  private http = inject(HttpClient);
  private router = inject(Router);

  private readonly apiUrl = 'http://127.0.0.1:8000/familias';

  familias = signal<Familia[]>([]);
  cargando = signal(false);
  guardando = signal(false);
  mostrarFormulario = signal(false);

  editandoId = signal<number | null>(null);
  eliminandoId = signal<number | null>(null);

  error = signal('');
  mensaje = signal('');

  nuevaFamilia = {
    responsable: '',
    sector: '',
    direccion: '',
    telefono: ''
  };

  ngOnInit(): void {
    this.cargarFamilias();
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

  private comprobarSesion(status: number): boolean {
    if (status === 401) {
      sessionStorage.removeItem('ecogestion_token');
      this.router.navigate(['/login']);
      return false;
    }

    return true;
  }

  // CONSULTAR familias
  cargarFamilias(): void {
    const headers = this.obtenerHeaders();
    if (!headers) return;

    this.cargando.set(true);
    this.error.set('');

    this.http.get<Familia[]>(
      this.apiUrl,
      { headers }
    ).subscribe({
      next: (datos) => {
        this.familias.set(datos);
        this.cargando.set(false);
      },
      error: (err) => {
        this.cargando.set(false);

        if (this.comprobarSesion(err.status)) {
          this.error.set('No se pudieron cargar las familias.');
        }
      }
    });
  }

  // ABRIR formulario para crear
  abrirFormulario(): void {
    this.editandoId.set(null);

    this.nuevaFamilia = {
      responsable: '',
      sector: '',
      direccion: '',
      telefono: ''
    };

    this.error.set('');
    this.mensaje.set('');
    this.mostrarFormulario.set(true);
  }

  // ABRIR formulario para editar
  editarFamilia(familia: Familia): void {
    this.editandoId.set(familia.id);

    this.nuevaFamilia = {
      responsable: familia.responsable,
      sector: familia.sector,
      direccion: familia.direccion,
      telefono: familia.telefono ?? ''
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

  // CREAR o ACTUALIZAR familia
  guardarFamilia(): void {
    const headers = this.obtenerHeaders();
    if (!headers || this.guardando()) return;

    const datos = {
      responsable: this.nuevaFamilia.responsable.trim(),
      sector: this.nuevaFamilia.sector.trim(),
      direccion: this.nuevaFamilia.direccion.trim(),
      telefono: this.nuevaFamilia.telefono.trim()
    };

    if (!datos.responsable || !datos.sector || !datos.direccion) {
      this.error.set('Completa los campos obligatorios.');
      return;
    }

    const id = this.editandoId();

    this.guardando.set(true);
    this.error.set('');

    const solicitud = id !== null
      ? this.http.put<Familia>(
          `${this.apiUrl}/${id}`,
          datos,
          { headers }
        )
      : this.http.post<Familia>(
          this.apiUrl,
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
            ? 'Familia actualizada correctamente.'
            : 'Familia registrada correctamente.'
        );

        this.cargarFamilias();
      },
      error: (err) => {
        this.guardando.set(false);

        if (this.comprobarSesion(err.status)) {
          this.error.set(
            'No se pudo guardar la familia. Código: ' + err.status
          );
        }
      }
    });
  }

  // ELIMINAR familia
  eliminarFamilia(familia: Familia): void {
    if (this.eliminandoId() !== null) return;

    const confirmar = window.confirm(
      `¿Estás seguro de eliminar a ${familia.responsable}?`
    );

    if (!confirmar) return;

    const headers = this.obtenerHeaders();
    if (!headers) return;

    this.eliminandoId.set(familia.id);
    this.error.set('');
    this.mensaje.set('');

    this.http.delete<void>(
      `${this.apiUrl}/${familia.id}`,
      { headers }
    ).subscribe({
      next: () => {
        this.eliminandoId.set(null);
        this.mensaje.set('Familia eliminada correctamente.');
        this.cargarFamilias();
      },
      error: (err) => {
        this.eliminandoId.set(null);

        if (this.comprobarSesion(err.status)) {
          this.error.set(
            'No se pudo eliminar la familia. Puede tener ' +
            'recolecciones asociadas. Código: ' + err.status
          );
        }
      }
    });
  }

  volverDashboard(): void {
    this.router.navigate(['/dashboard']);
  }
}
