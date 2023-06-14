import { ComponentFixture, TestBed } from '@angular/core/testing';

import { NewsProviderComponent } from './news-provider.component';

describe('NewsProviderComponent', () => {
  let component: NewsProviderComponent;
  let fixture: ComponentFixture<NewsProviderComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [NewsProviderComponent]
    });
    fixture = TestBed.createComponent(NewsProviderComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
