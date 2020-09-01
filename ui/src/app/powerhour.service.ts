import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable, of } from 'rxjs';

import { PowerHourJob } from './powerhour';
import { environment } from '../environments/environment';

@Injectable({
  providedIn: 'root',
})
export class PowerHourService {

  httpOptions = {
    headers: new HttpHeaders({ 'Content-Type': 'application/json' })
  };

  baseUrl = environment.apiUrl;

  constructor(private http: HttpClient) {
    console.log('env', environment.production);
  }

  getJob(jobId: string): Observable<any> {
    return this.http.get(this.baseUrl + '/jobs/' + jobId, this.httpOptions);
  }

  postJob(job: PowerHourJob): Observable<any> {
    console.log(job);
    return this.http.post(this.baseUrl + '/generate', job, this.httpOptions)
  }

  downloadPowerHour(jobId: string): Observable<Blob> {
    return this.http.get(this.baseUrl + '/jobs/' + jobId + '/download', {responseType: 'blob'});
  }

  private handleError<T>(operation = 'operation', result?: T) {
    return (error: any): Observable<T> => {

      // TODO: send the error to remote logging infrastructure
      console.error(error); // log to console instead

      // TODO: better job of transforming error for user consumption

      // Let the app keep running by returning an empty result.
      return of(result as T);
    };
  }
}
