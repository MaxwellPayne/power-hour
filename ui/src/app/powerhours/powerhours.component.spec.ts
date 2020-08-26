import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { PowerhoursComponent } from './powerhours.component';

describe('PowerhoursComponent', () => {
  let component: PowerhoursComponent;
  let fixture: ComponentFixture<PowerhoursComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ PowerhoursComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(PowerhoursComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
