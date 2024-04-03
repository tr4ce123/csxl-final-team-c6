import { ComponentFixture, TestBed } from '@angular/core/testing';

import { OrganizationApplicationComponent } from './organization-application.component';

describe('OrganizationApplicationComponent', () => {
  let component: OrganizationApplicationComponent;
  let fixture: ComponentFixture<OrganizationApplicationComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ OrganizationApplicationComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(OrganizationApplicationComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
