import { ComponentFixture, TestBed } from '@angular/core/testing';

import { OrganizationRosterComponent } from './organization-roster.component';

describe('OrganizationRosterComponent', () => {
  let component: OrganizationRosterComponent;
  let fixture: ComponentFixture<OrganizationRosterComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ OrganizationRosterComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(OrganizationRosterComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
