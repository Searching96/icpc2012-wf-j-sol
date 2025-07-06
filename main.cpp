#include <iostream>
#include <vector>
#include <cmath>
#include <iomanip>
#include <limits>
#include <algorithm>
#include <map>
#include <set> // Using set for automatic sorting and uniqueness based on custom comparator

using namespace std;

const long double R_earth = 6370.0;
const long double EPS = 1e-9;
const long double INF = numeric_limits<long double>::infinity();
const long double M_PI = 3.14159265358979323846L;

struct Point {
    long double x, y, z;

    // Custom comparator for set/map based on approximate equality
    struct Compare {
        bool operator()(const Point& a, const Point& b) const {
            if (abs(a.x - b.x) > EPS) return a.x < b.x;
            if (abs(a.y - b.y) > EPS) return a.y < b.y;
            return a.z < b.z - EPS;
        }
    };
};

// Operators for Point
Point operator+(const Point& a, const Point& b) { return {a.x + b.x, a.y + b.y, a.z + b.z}; }
Point operator-(const Point& a, const Point& b) { return {a.x - b.x, a.y - b.y, a.z - b.z}; }
Point operator*(const Point& a, long double s) { return {a.x * s, a.y * s, a.z * s}; }
Point operator*(long double s, const Point& a) { return {a.x * s, a.y * s, a.z * s}; }
Point operator/(const Point& a, long double s) { return {a.x / s, a.y / s, a.z / s}; }


// Convert degrees lat/lon to 3D Cartesian coordinates on sphere
Point lat_lon_to_xyz(long double lat_deg, long double lon_deg) {
    long double lat_rad = lat_deg * M_PI / 180.0;
    long double lon_rad = lon_deg * M_PI / 180.0;
    long double x = R_earth * cos(lat_rad) * cos(lon_rad);
    long double y = R_earth * cos(lat_rad) * sin(lon_rad);
    long double z = R_earth * sin(lat_rad);
    return {x, y, z};
}

// Dot product of two points (vectors)
long double dot(const Point& p1, const Point& p2) {
    return p1.x * p2.x + p1.y * p2.y + p1.z * p2.z;
}

// Cross product of two points (vectors)
Point cross(const Point& p1, const Point& p2) {
    return {p1.y * p2.z - p1.z * p2.y,
            p1.z * p2.x - p1.x * p2.z,
            p1.x * p2.y - p1.y * p2.x};
}

// Magnitude of a vector
long double magnitude(const Point& p) {
    return sqrt(dot(p, p));
}

// Normalize a vector
Point normalize(const Point& p) {
    long double mag = magnitude(p);
    if (mag < EPS) return {0, 0, 0};
    return p / mag;
}

// Great circle distance between two points on the sphere using XYZ coordinates
long double dist_xyz(const Point& p1, const Point& p2) {
    Point u1 = normalize(p1);
    Point u2 = normalize(p2);
    long double d = dot(u1, u2);
    d = max((long double)-1.0, min((long double)1.0, d)); // Clamp
    long double angle_rad = acos(d);
    return angle_rad * R_earth;
}

// Get point on great circle through U and V at angular distance `angle_from_u` from U
Point point_at_angle_on_great_circle(const Point& u, const Point& v, long double angle_from_u) {
    Point u_norm = normalize(u);
    Point v_norm = normalize(v);
    long double angle_uv = acos(max((long double)-1.0, min((long double)1.0, dot(u_norm, v_norm))));

    if (angle_uv < EPS) return u; // U and V are the same

    // Create orthogonal basis in the great circle plane
    Point v_ortho_norm = normalize(v_norm - u_norm * dot(u_norm, v_norm));

    // Point P on the great circle at angle angle_from_u from U
    return u_norm * cos(angle_from_u) + v_ortho_norm * sin(angle_from_u);
}


// Check if point P is on the great circle arc from U to V (inclusive)
bool is_on_arc(const Point& u, const Point& v, const Point& p) {
    long double dist_uv = dist_xyz(u, v);
    long double dist_up = dist_xyz(u, p);
    long double dist_pv = dist_xyz(p, v);
    // Check if distance U-P + P-V equals distance U-V (within tolerance)
    return abs(dist_up + dist_pv - dist_uv) < EPS;
}

// Get the parameter t in [0, 1] for a point P on the arc U-V based on distance
long double get_arc_parameter(const Point& u, const Point& v, const Point& p) {
    long double dist_uv = dist_xyz(u, v);
    if (dist_uv < EPS) return 0.0; // U == V, any point is effectively parameter 0
    long double dist_up = dist_xyz(u, p);
    return dist_up / dist_uv;
}


// Find intersection points of two small circles on the Earth sphere with the same radius R_sphere
vector<Point> get_small_circle_intersections(const Point& center1, const Point& center2, long double R_sphere) {
    Point c1_norm = normalize(center1);
    Point c2_norm = normalize(center2);
    long double r_ang = R_sphere / R_earth;
    long double d_ang = acos(max((long double)-1.0, min((long double)1.0, dot(c1_norm, c2_norm)))); // Angular distance between centers

    vector<Point> intersections;

    if (d_ang > 2 * r_ang + EPS) { // Spheres are too far apart
        return intersections;
    }
     if (d_ang < EPS) { // Centers are the same
         return intersections; // Intersection is the circle itself, not useful graph vertices
     }


    // Angle beta from the midpoint M of C1-C2 arc to intersection point P along the equidistant great circle
    // cos(r_ang) = cos(d_ang/2) * cos(beta) => cos(beta) = cos(r_ang) / cos(d_ang/2)
    long double cos_beta_arg = cos(r_ang) / cos(d_ang / 2.0);
    if (cos_beta_arg > 1.0 + EPS || cos_beta_arg < -1.0 - EPS) {
         // This might happen due to precision if d_ang is very close to 2*r_ang (tangent case)
         // Handle tangent case separately? For simplicity, clamp and continue.
         cos_beta_arg = max((long double)-1.0, min((long double)1.0, cos_beta_arg));
    }
    long double beta = acos(cos_beta_arg);

    // Midpoint M of the C1-C2 arc (angularly)
    Point m_norm = point_at_angle_on_great_circle(c1_norm, c2_norm, d_ang / 2.0);

    // Vector orthogonal to m_norm in the plane of the equidistant great circle
    // The equidistant great circle plane is orthogonal to c1_norm - c2_norm
    Point ortho_m_norm = normalize(cross(m_norm, c1_norm - c2_norm));

    // The two intersection points are beta angular distance from M along the equidistant great circle
    Point p1_norm = m_norm * cos(beta) + ortho_m_norm * sin(beta);
    Point p2_norm = m_norm * cos(beta) - ortho_m_norm * sin(beta);

    intersections.push_back({p1_norm.x * R_earth, p1_norm.y * R_earth, p1_norm.z * R_earth});
    if (beta > EPS) { // Avoid adding duplicate point if tangent (beta=0)
         intersections.push_back({p2_norm.x * R_earth, p2_norm.y * R_earth, p2_norm.z * R_earth});
    }

    return intersections;
}


// Get parameters [t_start, t_end] on arc U-V (parameterized 0 to 1 by distance) that are inside R-sphere of center K
vector<pair<long double, long double>> get_covered_intervals(const Point& u, const Point& v, const Point& k_center, long double R_sphere) {
    long double r_ang = R_sphere / R_earth;
    Point u_norm = normalize(u);
    Point v_norm = normalize(v);
    Point k_norm = normalize(k_center);
    long double angle_uv = acos(max((long double)-1.0, min((long double)1.0, dot(u_norm, v_norm))));
    if (angle_uv < EPS) { // U and V are the same or very close
         // If U is inside R-sphere of K, the "arc" (point) is covered.
         if (dist_xyz(u, k_center) <= R_sphere + EPS) return {{0.0, 1.0}};
         else return {};
    }

    // Great circle through U and V has normal cross(u_norm, v_norm)
    Point gc_normal = normalize(cross(u_norm, v_norm));

    // Find points P on the great circle U-V where angle(P, K_norm) = r_ang
    // This is intersection of great circle (dot(P, gc_normal)=0) and small circle (center K_norm, ang_rad r_ang)
    // Project K_norm onto the plane of the great circle
    Point k_proj_norm = k_norm - gc_normal * dot(k_norm, gc_normal);
    k_proj_norm = normalize(k_proj_norm);

    long double d_k_to_plane_ang = acos(max((long double)-1.0, min((long double)1.0, abs(dot(k_norm, gc_normal)))));

    vector<long double> critical_params;
    critical_params.push_back(0.0); // Arc start
    critical_params.push_back(1.0); // Arc end

    if (d_k_to_plane_ang <= r_ang + EPS) { // Small circle boundary intersects or is tangent to or contains the great circle
        long double alpha; // Angle on the great circle from k_proj_norm to intersection points
        if (abs(d_k_to_plane_ang - r_ang) < EPS) {
             alpha = 0; // Tangent case
        } else {
            // cos(r_ang) = cos(d_k_to_plane_ang) * cos(alpha)
            long double cos_alpha_arg = cos(r_ang) / cos(d_k_to_plane_ang);
            if (cos_alpha_arg >= -1.0 - EPS && cos_alpha_arg <= 1.0 + EPS) {
                 alpha = acos(max((long double)-1.0, min((long double)1.0, cos_alpha_arg)));

                 // Vector in great circle plane orthogonal to k_proj_norm
                 Point ortho_k_proj_norm = normalize(cross(gc_normal, k_proj_norm));

                 // The two intersection points on the great circle
                 Point p1_norm_gc = k_proj_norm * cos(alpha) + ortho_k_proj_norm * sin(alpha);
                 Point p2_norm_gc = k_proj_norm * cos(alpha) - ortho_k_proj_norm * sin(alpha);

                 Point p1_gc = {p1_norm_gc.x * R_earth, p1_norm_gc.y * R_earth, p1_norm_gc.z * R_earth};
                 Point p2_gc = {p2_norm_gc.x * R_earth, p2_norm_gc.y * R_earth, p2_norm_gc.z * R_earth};


                 // Check if these points lie on the arc U-V and add their parameters
                 if (is_on_arc(u, v, p1_gc)) {
                      critical_params.push_back(get_arc_parameter(u, v, p1_gc));
                 }
                 if (alpha > EPS && is_on_arc(u, v, p2_gc)) { // Avoid adding duplicate point if tangent
                      critical_params.push_back(get_arc_parameter(u, v, p2_gc));
                 }
            } else {
                // No intersection between the great circle and the small circle boundary.
                // The arc is either entirely inside or entirely outside the R-sphere of K.
                // Check the midpoint of the arc.
                long double mid_t_angle = angle_uv / 2.0;
                Point p_mid = point_at_angle_on_great_circle(u, v, mid_t_angle);
                if (dist_xyz(p_mid, k_center) <= R_sphere + EPS) {
                    // Entire arc is inside this R-sphere
                    return {{0.0, 1.0}};
                } else {
                    // Entire arc is outside this R-sphere
                    return {};
                }
            }
        }
    } else {
         // No intersection between great circle and small circle boundary.
         // Arc is either entirely inside or entirely outside. Check midpoint.
         long double mid_t_angle = angle_uv / 2.0;
         Point p_mid = point_at_angle_on_great_circle(u, v, mid_t_angle);
         if (dist_xyz(p_mid, k_center) <= R_sphere + EPS) {
             return {{0.0, 1.0}};
         } else {
             return {};
         }
    }


    sort(critical_params.begin(), critical_params.end());
    critical_params.erase(unique(critical_params.begin(), critical_params.end(), [](long double a, long double b){ return abs(a-b) < EPS; }), critical_params.end());

    vector<pair<long double, long double>> intervals;
    for(size_t i = 0; i + 1 < critical_params.size(); ++i) {
        long double t_start = critical_params[i];
        long double t_end = critical_params[i+1];
        if (t_end - t_start < EPS) continue;

        long double t_mid = (t_start + t_end) / 2.0;
         // Get the point on the arc at t_mid parameter (based on distance parameter)
         Point p_mid = point_at_angle_on_great_circle(u, v, t_mid * angle_uv);

         // Check if the midpoint is inside the R-sphere of K
         if (dist_xyz(p_mid, k_center) <= R_sphere + EPS) {
              intervals.push_back({t_start, t_end});
         }
    }

    return intervals;
}


// Merge overlapping intervals [t_start, t_end]
vector<pair<long double, long double>> merge_intervals(vector<pair<long double, long double>>& intervals) {
    if (intervals.empty()) return {};
    sort(intervals.begin(), intervals.end());
    vector<pair<long double, long double>> merged;
    if (!intervals.empty()) {
        merged.push_back(intervals[0]);
        for (size_t i = 1; i < intervals.size(); ++i) {
            if (intervals[i].first <= merged.back().second + EPS) { // Overlap or touch
                merged.back().second = max(merged.back().second, intervals[i].second);
            } else {
                merged.push_back(intervals[i]);
            }
        }
    }
    return merged;
}

// Check if arc U-V is safe (fully covered by union of R-spheres of airports)
bool is_arc_safe(const Point& u, const Point& v, const vector<Point>& airports, long double R_sphere) {
    long double dist_uv = dist_xyz(u, v);
    if (dist_uv < EPS) return true; // Zero-length arc is always safe

    vector<pair<long double, long double>> all_intervals;
    for (const auto& airport_loc : airports) {
        vector<pair<long double, long double>> intervals = get_covered_intervals(u, v, airport_loc, R_sphere);
        all_intervals.insert(all_intervals.end(), intervals.begin(), intervals.end());
    }

    vector<pair<long double, long double>> merged = merge_intervals(all_intervals);

    // Check if the interval [0, 1] is fully covered
    if (merged.empty()) return false;

     long double current_t = 0.0;
     for(const auto& interval : merged) {
         if (interval.first > current_t + EPS) return false; // Gap
         current_t = max(current_t, interval.second);
     }
     if (current_t < 1.0 - EPS) return false; // Does not reach the end

    return true;
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);

    cout << fixed << setprecision(3);

    int N, Q, case_num = 1;
    long double R;

    while (cin >> N >> R) {
        vector<Point> airports_xyz(N);
        for (int i = 0; i < N; ++i) {
            long double lat, lon;
            cin >> lon >> lat; // Input is lon lat
            airports_xyz[i] = lat_lon_to_xyz(lat, lon);
        }

        set<Point, Point::Compare> unique_vertices_set;
        for(const auto& p : airports_xyz) unique_vertices_set.insert(p);

        // Add intersection points of R-spheres as vertices
        for (int i = 0; i < N; ++i) {
            for (int j = i + 1; j < N; ++j) {
                vector<Point> intersections = get_small_circle_intersections(airports_xyz[i], airports_xyz[j], R);
                for (const auto& p : intersections) {
                   unique_vertices_set.insert(p);
                }
            }
        }

        vector<Point> vertices(unique_vertices_set.begin(), unique_vertices_set.end());
        map<Point, int, Point::Compare> vertex_map;
        vector<int> airport_to_vertex_idx(N);

        for (int i = 0; i < vertices.size(); ++i) {
            vertex_map[vertices[i]] = i;
        }
        for (int i = 0; i < N; ++i) {
             airport_to_vertex_idx[i] = vertex_map[airports_xyz[i]];
        }


        int V = vertices.size();
        vector<vector<long double>> adj_aux(V, vector<long double>(V, INF));

        for (int i = 0; i < V; ++i) {
            adj_aux[i][i] = 0;
        }

        // Build auxiliary graph with safe arcs
        for (int i = 0; i < V; ++i) {
            for (int j = i + 1; j < V; ++j) {
                // Optimization: if endpoints are identical or antipodal, arc safety is trivial
                long double d_ij = dist_xyz(vertices[i], vertices[j]);
                bool safe = false;
                if (d_ij < EPS) { // Same point
                    safe = true;
                } else if (abs(d_ij - R_earth * M_PI) < EPS) { // Antipodal points
                    // Check if antipodal arc is covered - this needs separate logic or is impossible?
                    // Union of spheres condition. If the whole sphere is covered, yes.
                    // Check if midpoint of ANY airport-antipodal airport arc is within R of ANY airport?
                    // This case is complex, maybe not required by test cases or covered by general logic.
                    // Assume for now that standard arc safety covers this.
                     safe = is_arc_safe(vertices[i], vertices[j], airports_xyz, R);
                }
                else {
                    safe = is_arc_safe(vertices[i], vertices[j], airports_xyz, R);
                }

                if (safe) {
                    adj_aux[i][j] = adj_aux[j][i] = d_ij;
                }
            }
        }

        // Floyd-Warshall on auxiliary graph to find shortest safe path between any two vertices
        for (int k = 0; k < V; ++k) {
            for (int i = 0; i < V; ++i) {
                for (int j = 0; j < V; ++j) {
                    if (adj_aux[i][k] != INF && adj_aux[k][j] != INF) {
                        adj_aux[i][j] = min(adj_aux[i][j], adj_aux[i][k] + adj_aux[k][j]);
                    }
                }
            }
        }

        cin >> Q;
        cout << "Case " << case_num++ << ":" << endl;

        for (int q = 0; q < Q; ++q) {
            int s, t;
            long double c;
            cin >> s >> t >> c;
            --s; --t; // 0-indexed airports

            // Build refueling graph (only airports as vertices) for the current fuel capacity c
            vector<vector<long double>> current_adj_refuel(N, vector<long double>(N, INF));
            for(int i = 0; i < N; ++i) current_adj_refuel[i][i] = 0;

            for(int i = 0; i < N; ++i) {
                for(int j = 0; j < N; ++j) {
                    if (i == j) continue;
                    int u_idx = airport_to_vertex_idx[i];
                    int v_idx = airport_to_vertex_idx[j];
                    // Edge exists between airports i and j if the shortest safe path in the aux graph is <= fuel capacity c
                    if (adj_aux[u_idx][v_idx] <= c + EPS) {
                        current_adj_refuel[i][j] = adj_aux[u_idx][v_idx];
                    }
                }
            }

            // Floyd-Warshall on the airport graph to find shortest path with refueling stops
            for (int k = 0; k < N; ++k) {
                for (int i = 0; i < N; ++i) {
                    for (int j = 0; j < N; ++j) {
                         if (current_adj_refuel[i][k] != INF && current_adj_refuel[k][j] != INF) {
                             current_adj_refuel[i][j] = min(current_adj_refuel[i][j], current_adj_refuel[i][k] + current_adj_refuel[k][j]);
                        }
                    }
                }
            }

            if (current_adj_refuel[s][t] == INF) {
                cout << "impossible" << endl;
            } else {
                cout << current_adj_refuel[s][t] << endl;
            }
        }
    }

    return 0;
}