import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable, of } from 'rxjs';
import { catchError, map, tap } from 'rxjs/operators';

import { PowerHourJob } from './powerhour';

@Injectable({
  providedIn: 'root',
})
export class PowerHourService {

  httpOptions = {
    headers: new HttpHeaders({ 'Content-Type': 'application/json' })
  };

  baseUrl = 'http://localhost:8000';

  constructor(private http: HttpClient) { }

  getJob(jobId: string): Observable<any> {
    return this.http.get(this.baseUrl + '/jobs/' + jobId, this.httpOptions);
  }

  postJob(job: PowerHourJob): Observable<any> {
    console.log(job);
    return this.http.post(this.baseUrl + '/generate', job, this.httpOptions)
      //.pipe(
      //  catchError(this.handleError<PowerHourJob>('postJob', null))
      //)
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
