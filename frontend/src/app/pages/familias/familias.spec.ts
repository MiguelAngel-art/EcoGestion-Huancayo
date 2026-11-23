import { ComponentFixture, TestBed } from '@angular/core/testing';
import { Familias } from './familias';

describe('Familias', () => {
  let component: Familias;
  let fixture: ComponentFixture<Familias>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [Familias],
    }).compileComponents();

    fixture = TestBed.createComponent(Familias);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
