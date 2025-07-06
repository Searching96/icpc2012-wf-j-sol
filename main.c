#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <float.h>
#include <string.h>
#define MAXN 25
#define PI 3.14159265358979323846
#define MAXV 700 // At most N + 2*(N choose 2) <= 25 + 600 = 625 nodes
#define INF 1e100
static const double EARTH_R = 6370.0;

typedef struct { double x,y,z; } Vec;

// dot product
static double dot(const Vec *a,const Vec *b){
    return a->x*b->x + a->y*b->y + a->z*b->z;
}
// cross product a x b -> out
static void cross(const Vec *a,const Vec *b, Vec *out){
    out->x = a->y*b->z - a->z*b->y;
    out->y = a->z*b->x - a->x*b->z;
    out->z = a->x*b->y - a->y*b->x;
}
// norm
static double norm(const Vec *a){
    return sqrt(dot(a,a));
}
// scale v by s
static void scale(Vec *v,double s){
    v->x*=s; v->y*=s; v->z*=s;
}
// add a+b -> out
static void addv(const Vec *a,const Vec *b, Vec *out){
    out->x = a->x + b->x;
    out->y = a->y + b->y;
    out->z = a->z + b->z;
}
// subtract a-b -> out
static void subv(const Vec *a,const Vec *b, Vec *out){
    out->x = a->x - b->x;
    out->y = a->y - b->y;
    out->z = a->z - b->z;
}
// normalize in-place
static void normalize(Vec *v){
    double n = norm(v);
    if(n>0) scale(v,1.0/n);
}
// convert (lon,lat) degrees to unit sphere vector
static void sph2vec(double lon_deg,double lat_deg, Vec *v){
    double lon = lon_deg*PI/180.0;
    double lat = lat_deg*PI/180.0;
    double cl = cos(lat), sl = sin(lat);
    v->x = cl * cos(lon);
    v->y = cl * sin(lon);
    v->z = sl;
}

// comparison function for qsort
static int compare_intervals(const void *a, const void *b) {
    const double *ia = (const double *)a;
    const double *ib = (const double *)b;
    if (ia[0] < ib[0]) return -1;
    if (ia[0] > ib[0]) return 1;
    return 0;
}

int main(){
    int N, caseNo=1;
    while(scanf("%d",&N)==1){
        int R; 
        if(N==0) break;
        scanf("%d",&R);
        Vec airports[MAXN];
        for(int i=0;i<N;i++){
            double lon,lat;
            scanf("%lf%lf",&lon,&lat);
            sph2vec(lon,lat,&airports[i]);
        }
        // angular radius
        double alpha = (double)R / EARTH_R;
        double cosA = cos(alpha);

        // build node list
        Vec V[MAXV];
        int isAirport[MAXV]={0};
        int Vn = 0;
        for(int i=0;i<N;i++){
            V[Vn] = airports[i];
            isAirport[Vn++] = 1;
        }
        // intersections of safety-circle boundaries
        for(int i=0;i<N;i++) for(int j=i+1;j<N;j++){
            Vec *u = &airports[i], *v = &airports[j];
            double cuv = dot(u,v);
            // need two circles of radius alpha to intersect: cuv in [cos(2α),1)
            if(cuv < cos(2*alpha)-1e-12) continue;
            // solve p = A u + B v, with A=B
            double Delta = 1.0 - cuv*cuv;
            if(Delta < 1e-15) continue;
            double k = cosA*(1.0 - cuv)/Delta;
            Vec p;
            p.x = k*(u->x + v->x);
            p.y = k*(u->y + v->y);
            p.z = k*(u->z + v->z);
            double p2 = dot(&p,&p);
            double h2 = 1.0 - p2;
            if(h2 < 0) h2 = 0;
            double h = sqrt(h2);
            Vec n;
            cross(u,v,&n);
            double nl = norm(&n);
            if(nl < 1e-15) continue;
            scale(&n, 1.0/nl);
            // two intersection points p±h*n
            Vec i1 = p, i2 = p;
            scale(&n,h);
            addv(&i1,&n,&i1);
            subv(&i2,&n,&i2);
            normalize(&i1);
            normalize(&i2);
            V[Vn++] = i1;
            V[Vn++] = i2;
        }
        // prepare adjacency: initially INF
        static double D[MAXV][MAXV];
        for(int i=0;i<Vn;i++) for(int j=0;j<Vn;j++)
            D[i][j] = (i==j? 0.0 : INF);

        // For each pair of nodes a,b, test whether arc lies inside union of caps
        // We'll parameterize arc from a->b by angle θ in [0,θ_ab], and for each airport
        // compute the interval of θ for which dot(P(θ),Ai)>=cosA, build union and check cover.
        Vec abU, abW;
        for(int a=0;a<Vn;a++) for(int b=a+1;b<Vn;b++){
            // great circle angle between V[a],V[b]
            double cab = dot(&V[a],&V[b]);
            if(cab>1) cab=1; else if(cab<-1) cab=-1;
            double theta_ab = acos(cab);
            if(theta_ab<1e-12) continue;
            // unit orthonormal basis in plane: U=V[a], W=(V[b]-U*cab)/sinθ
            abU = V[a];
            Vec tmp; subv(&V[b],&abU,&tmp);
            scale(&tmp, 1.0/sin(theta_ab));
            abW = tmp;
            // gather coverage intervals on [0,θ_ab]
            // at most N intervals
            static double ivs[2*MAXN][2];
            int ivn=0;
            for(int i=0;i<N;i++){
                // we want dot( cosθ U + sinθ W , Ai ) >= cosA
                // i.e. cosθ*du + sinθ*dw >= cosA, where du=dot(U,Ai), dw=dot(W,Ai)
                double du = dot(&abU,&airports[i]);
                double dw = dot(&abW,&airports[i]);
                // solve du*cosθ + dw*sinθ >= cosA
                // this is R*cos(θ-φ) >= cosA, where R = sqrt(du^2+dw^2), φ=atan2(dw,du)
                double Rv = sqrt(du*du+dw*dw);
                if(Rv < 1e-15) continue;
                if(Rv < cosA) continue; // no solutions
                double phi = atan2(dw,du);
                double delta = acos(cosA / Rv);
                double t1 = phi - delta;
                double t2 = phi + delta;
                // normalize into [0,2π)
                while(t1<0) t1 += 2*PI;
                while(t1>2*PI) t1 -= 2*PI;
                while(t2<0) t2 += 2*PI;
                while(t2>2*PI) t2 -= 2*PI;
                // intersect [t1,t2] with [0,θ_ab]
                // but θ_ab <= π so at most wrap once
                if(t1 <= t2){
                    if(t2 < 0 || t1 > theta_ab) continue;
                    ivs[ivn][0] = fmax(0.0,t1);
                    ivs[ivn][1] = fmin(theta_ab,t2);
                    ivn++;
                } else {
                    // wraps around: [t1,2π) and [0,t2]
                    if(t1 <= theta_ab){
                        ivs[ivn][0] = t1;
                        ivs[ivn][1] = theta_ab;
                        ivn++;
                    }
                    if(t2 >= 0){
                        double uu = fmax(0.0,0.0);
                        double vv = fmin(theta_ab,t2);
                        if(vv>uu){
                            ivs[ivn][0] = uu;
                            ivs[ivn][1] = vv;
                            ivn++;
                        }
                    }
                }
            }
            // merge intervals over [0,θ_ab]
            if(ivn==0) continue;
            qsort(ivs,ivn,sizeof(ivs[0]), compare_intervals);
            double reach = 0;
            int idx=0;
            while(idx<ivn && ivs[idx][0] <= reach + 1e-12){
                double best = reach;
                while(idx<ivn && ivs[idx][0] <= reach + 1e-12){
                    if(ivs[idx][1] > best) best = ivs[idx][1];
                    idx++;
                }
                reach = best;
                if(reach >= theta_ab - 1e-12) break;
            }
            if(reach >= theta_ab - 1e-12){
                // covered => valid edge
                double dist_km = theta_ab * EARTH_R;
                D[a][b] = D[b][a] = dist_km;
            }
        }

        // Floyd–Warshall on node graph
        for(int k=0;k<Vn;k++)
        for(int i=0;i<Vn;i++){
            if(D[i][k]>=INF) continue;
            for(int j=0;j<Vn;j++){
                double via = D[i][k] + D[k][j];
                if(via < D[i][j]) D[i][j] = via;
            }
        }

        // Extract airport-to-airport distances
        static double AtoA[MAXN][MAXN];
        for(int i=0;i<N;i++) for(int j=0;j<N;j++){
            AtoA[i][j] = D[i][j];
        }

        // handle queries
        int Q; scanf("%d",&Q);
        printf("Case %d:\n",caseNo++);
        while(Q--){
            int s,t; double c;
            scanf("%d%d%lf",&s,&t,&c);
            s--; t--;
            // Dijkstra on N airports using edges AtoA[i][j] if <=c
            static double distN[MAXN];
            static int used[MAXN];
            for(int i=0;i<N;i++){
                distN[i] = (i==s? 0.0: INF);
                used[i]=0;
            }
            for(int it=0;it<N;it++){
                int u=-1; double best=INF;
                for(int i=0;i<N;i++) if(!used[i] && distN[i]<best){
                    best=distN[i]; u=i;
                }
                if(u<0) break;
                used[u]=1;
                for(int v=0;v<N;v++){
                    double w = AtoA[u][v];
                    if(w<=c+1e-9 && distN[u]+w < distN[v]){
                        distN[v] = distN[u]+w;
                    }
                }
            }
            if(distN[t]>=INF/2){
                printf("impossible\n");
            } else {
                printf("%.3f\n",distN[t]);
            }
        }
        fflush(stdout);
    }
    return 0;
}
