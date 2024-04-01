import { ComponentFixture, TestBed } from '@angular/core/testing';

import { OrganizationApplicantsComponent } from './organization-applicants.component';

describe('OrganizationApplicantsComponent', () => {
  let component: OrganizationApplicantsComponent;
  let fixture: ComponentFixture<OrganizationApplicantsComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ OrganizationApplicantsComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(OrganizationApplicantsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
