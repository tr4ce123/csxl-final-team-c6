/**
 * The Organization Routing Module holds all of the routes that are children
 * to the path /organizations/...
 *
 * @author Ajay Gandecha, Jade Keegan, Brianna Ta, Audrey Toney
 * @copyright 2023
 * @license MIT
 */

import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { OrganizationPageComponent } from './organization-page/organization-page.component';
import { OrganizationDetailsComponent } from './organization-details/organization-details.component';
import { OrganizationEditorComponent } from './organization-editor/organization-editor.component';
import { OrganizationApplicantsComponent } from './organization-applicants/organization-applicants.component';
import { OrganizationRosterComponent } from './organization-roster/organization-roster.component';
import { OrganizationApplicationComponent } from './organization-application/organization-application.component';
import { OrganizationEditMemberComponent } from './organization-edit-member/organization-edit.component';

const routes: Routes = [
  OrganizationPageComponent.Route,
  OrganizationDetailsComponent.Route,
  OrganizationEditorComponent.Route,
  OrganizationApplicantsComponent.Route,
  OrganizationRosterComponent.Route,
  OrganizationApplicationComponent.Route,
  OrganizationEditMemberComponent.Route
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class OrganizationRoutingModule {}
