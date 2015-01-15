#include <iostream>
#include <vector>
#include <list>
#include <cstdlib>
#include <cstdio>
#include <sstream>
#include <algorithm>
using namespace std;

struct process {
    int i, pi, ri;
    process() {
        i = -1; pi = 0; ri = 0;
    }
    process( int _i, int _pi, int _ri ) {
        i = _i; pi=_pi; ri=_ri;
    }
    process( const process& _p ) {
        i = _p.i; pi = _p.pi; ri = _p.ri;
    }
    int tick() { return --ri; }
    bool operator<(const process& _p) {
        if( -1 == _p.i ) return true;
        if( -1 == i ) return false;
        return i < _p.i;
    }
};

bool cmp_priority( const process& _p1, const process& _p2 ) {
    return _p1.pi > _p2.pi;
}

bool is_done( const std::vector<process>& v ) {
    for( auto it = v.begin(); it != v.end(); ++it ) if( -1 != it->i ) return false;
    return true;
}

int main(int argc, char *argv[]) {
    if( argc < 3 ) {
        std::cerr << "Two arguments expected!\n";
        return 1;
    }
    /*
       0 - strategia FCFS (bez wywłaszczania)
       1 - strategia SJF (bez wywłaszczania)
       2 - strategia SRTF (z wywłaszczaniem)
       3 - strategia RR (z wywłaszczaniem)
       4 - szeregowanie priorytetowe z wywłaszczaniem, zadania o takich samych priorytetach szeregowane algorytmem FCFS
       5 - szeregowanie priorytetowe z wywłaszczaniem, zadania o takich samych priorytetach szeregowane algorytmem SRTF
       6 - szeregowanie priorytetowe bez wywłaszczania, zadania o takich samych priorytetach szeregowane algorytmem FCFS
       */
    std::list<process> queue;
    std::vector<process> resources( atoi( argv[2] ) );
    char buf[80];
    int t = -1;
    int q = ( argc == 4 ? atoi( argv[3] ) : 1 );

    switch( atoi( argv[1] ) ) {
        case 0: {
                    while( std::cin.good() || !is_done(resources) ) {
                        std::cin.getline( buf, sizeof(buf) );
                        std::istringstream is( buf );
                        int dupa;
                        if(is.good()) is >> dupa;
                        while( is.good() ) {
                            struct process tmp(-1, 0, 0);
                            is >> tmp.i >> tmp.pi >> tmp.ri;
                            if( -1 != tmp.i ) queue.push_back( tmp );
                        }
                        std::cout << ++t;
                        for( auto it = resources.begin(); it != resources.end(); ++it ) {
                            if( -1 == it->i || 0 == --it->ri ) {
                                if( queue.empty() ) it->i = -1;
                                else {
                                    *it = queue.front();
                                    queue.pop_front();
                                }
                            }
                        }
                        std::sort( resources.begin(), resources.end() );
                        for( auto it = resources.begin(); it != resources.end(); ++it )
                            std::cout << " " << it->i;
                        std::cout << std::endl;
                    }
                    break;
                }
        case 2: {
                    int counter = 0;
                    while( std::cin.good() || !is_done(resources) ) {
                        std::cin.getline( buf, sizeof(buf) );
                        std::istringstream is( buf );
                        int dupa;
                        if(is.good()) is >> dupa;
                        while( is.good() ) {
                            struct process tmp(-1, 0, 0);
                            is >> tmp.i >> tmp.pi >> tmp.ri;
                            if( -1 != tmp.i ) queue.push_back( tmp );
                        }
                        std::cout << ++t;
                        for( auto it = resources.begin(); it != resources.end(); ++it ) {
                            if( -1 == it->i || 0 == --it->ri || counter % q) {
                                if( queue.empty() ) it->i = -1;
                                else {
                                    std::list<process>::iterator min = queue.begin();
                                    for( auto e = queue.begin(); e != queue.end(); ++e )
                                        if( e->ri < min->ri ) min = e;
                                    if( -1 != it->i && 0 != it->ri ) queue.push_back( *it );
                                    *it = *min;
                                    queue.erase( min );
                                }
                            }
                        }
                        std::sort( resources.begin(), resources.end() );
                        for( auto it = resources.begin(); it != resources.end(); ++it )
                            std::cout << " " << it->i;
                        std::cout << std::endl;
                        ++counter;
                    }
                    break;
                }
        case 4: {
                    int counter = 0;
                    while( std::cin.good() || !is_done(resources) ) {
                        std::cin.getline( buf, sizeof(buf) );
                        std::istringstream is( buf );
                        int dupa;
                        if(is.good()) is >> dupa;
                        while( is.good() ) {
                            struct process tmp(-1, 0, 0);
                            is >> tmp.i >> tmp.pi >> tmp.ri;
                            if( -1 != tmp.i ) queue.push_back( tmp );
                        }
                        std::cout << ++t;
                        for( auto it = resources.begin(); it != resources.end(); ++it ) {
                            if( -1 == it->i || 0 == --it->ri || counter % q) {
                                if( queue.empty() ) it->i = -1;
                                else {
                                    std::list<process>::iterator max = queue.begin();
                                    for( auto e = queue.begin(); e != queue.end(); ++e )
                                        if( e->pi > max->pi ) max = e;
                                    if( -1 != it->i && 0 != it->ri ) queue.push_front( *it );
                                    *it = *max;
                                    queue.erase( max );
                                }
                            }
                        }
                        std::sort( resources.begin(), resources.end() );
                        for( auto it = resources.begin(); it != resources.end(); ++it )
                            std::cout << " " << it->i;
                        std::cout << std::endl;
                        ++counter;
                    }
                    break;
                }
        case 5: {
                    int counter = 0;
                    while( std::cin.good() || !is_done(resources) ) {
                        std::cin.getline( buf, sizeof(buf) );
                        std::istringstream is( buf );
                        int dupa;
                        if(is.good()) is >> dupa;
                        while( is.good() ) {
                            struct process tmp(-1, 0, 0);
                            is >> tmp.i >> tmp.pi >> tmp.ri;
                            if( -1 != tmp.i ) queue.push_back( tmp );
                            queue.sort(cmp_priority);
                        }
                        std::cout << ++t;
                        for( auto it = resources.begin(); it != resources.end(); ++it ) {
                            if( -1 == it->i || 0 == --it->ri || counter % q) {
                                if( queue.empty() ) it->i = -1;
                                else {
                                    std::list<process>::iterator max = queue.begin(), min = queue.begin();
                                    for( auto e = queue.begin(); e != queue.end(); ++e )
                                        if( e->pi != max->pi ) max = e;
                                    for( auto e = queue.begin(); e != max; ++e )
                                        if( e->ri < min->ri ) min = e;
                                    if( -1 != it->i && 0 != it->ri ) queue.push_front( *it );
                                    queue.sort(cmp_priority);
                                    *it = *max;
                                    queue.erase( max );
                                }
                            }
                        }
                        std::sort( resources.begin(), resources.end() );
                        for( auto it = resources.begin(); it != resources.end(); ++it )
                            std::cout << " " << it->i;
                        std::cout << std::endl;
                        ++counter;
                    }
                    break;
                }
        default:
                std::cerr << "Not implemented\n";
    }

    return 0;
}
