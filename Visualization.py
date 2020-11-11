import plotly as py
import plotly.graph_objects as go
import numpy as np

def get_b1(b0, b2):
    # b0, b1 list of x, y coordinates
    if len(b0) != len(b2) != 2:
        raise ValueError('b0, b1 must be lists of two elements')
    b1 = 0.5 * (np.asarray(b0)+np.asarray(b2))+\
         0.5 * np.array([0,1.0]) * np.sqrt(3) * np.linalg.norm(np.array(b2)-np.array(b0))
    return b1.tolist() 


def dim_plus_1(b, w):#lift the points b0, b1, b2 to 3D points a0, a1, a2 (see Gallier book)
    #b is a list of 3 lists of 2D points, i.e. a list of three 2-lists 
    #w is a list of numbers (weights) of len equal to the len of b
    if not isinstance(b, list) or  not isinstance(b[0], list):
        raise ValueError('b must be a list of three 2-lists')
    if len(b) != len(w)   != 3:
        raise ValueError('the number of weights must be  equal to the nr of points')
    else:
        a = np.array([point + [w[i]] for (i, point) in enumerate(b)])
        a[1, :2] *= w[1]
        return a
    
def Bezier_curve(bz, nr): #the control point coordinates are passed in a list bz=[bz0, bz1, bz2] 
    # bz is a list of three 2-lists 
    # nr is the number of points to be computed on each arc
    t = np.linspace(0, 1, nr)
    #for each parameter t[i] evaluate a point on the Bezier curve with the de Casteljau algorithm
    N = len(bz) 
    points = [] # the list of points to be computed on the Bezier curve
    for i in range(nr):
        aa = np.copy(bz) 
        for r in range(1, N):
            aa[:N-r,:] = (1-t[i]) * aa[:N-r,:] + t[i] * aa[1:N-r+1,:]  # convex combination of points
        points.append(aa[0,:])                                  
    return np.array(points)

def Rational_Bezier_curve(a, nr):
    discrete_curve = Bezier_curve(a, nr ) 
    return [p[:2]/p[2] for p in discrete_curve]

pl_density = [[0.0, 'rgb(230,240,240)'],
              [0.1, 'rgb(187,220,228)'],
              [0.2, 'rgb(149,197,226)'],
              [0.3, 'rgb(123,173,227)'],
              [0.4, 'rgb(115,144,227)'],
              [0.5, 'rgb(119,113,213)'],
              [0.6, 'rgb(120,84,186)'],
              [0.7, 'rgb(115,57,151)'],
              [0.8, 'rgb(103,35,112)'],
              [0.9, 'rgb(82,20,69)'],
              [1.0, 'rgb(54,14,36)']]
def arc_plot(diagonal, recorte = 43, arc_num = 20, arc_size = 0.33):
    data = []
    tooltips = [] #list of strings to be displayed when hovering the mouse over the middle of the circle arcs
    xx = []
    yy = []
    
    diagonal_val = diagonal[:arc_num]
    for i in range(len(diagonal_val)):
        diagonal_val[i][0][0] = diagonal_val[i][0][0]//recorte
        diagonal_val[i][0][1] = diagonal_val[i][0][1]//recorte
        diagonal_val[i][1]  = diagonal_val[i][1]//recorte
    diagonal_val.sort(key= lambda x:x[0][0])
    indices = []
    for i in range(len(diagonal_val)):
        indices.append(diagonal_val[i][0][0])
        indices.append(diagonal_val[i][0][1])
        indices = list(set(indices))
    indices.sort()
    tempo = [f'{indices[k]} segundos' for k in range(len(indices))]
    links = [(diagonal_val[j][0][0], diagonal_val[j][0][1]) for j in range (len(diagonal_val))]
    
    size_diag = [diagonal_val[p][1] for p in range(len(diagonal_val))]
    
    node_trace = dict(type='scatter',
                  x=list(range(len(indices))),
                  y=[0]*len(indices),
                  mode='markers',
                  marker=dict(size=12, 
                              color='rgb(149,197,226)', 
                              colorscale=pl_density,
                              showscale=False,
                              line=dict(color='rgb(50,50,50)', width=0.75)),
                  text=tempo,
                  hoverinfo='text')
    
    X = list(range(len(indices))) # node x-coordinates
    nr = 75 
    for i in range(len(links)):
        tooltips.append(f'tempo de({links[i][0]} até {links[i][1]})={size_diag[i]}')
        j = indices.index(links[i][0])
        k = indices.index(links[i][1])
        b0 = [X[j], 0.0]
        b2 = [X[k], 0.0]
        b1 = get_b1(b0, b2)
        a = dim_plus_1([b0, b1, b2], [1, 0.5, 1])
        pts = Rational_Bezier_curve(a, nr)
        xx.append(pts[nr//2][0]) #abscissa of the middle point on the computed arc
        yy.append(pts[nr//2][1]) #ordinate of the same point
        x,y = zip(*pts)
    
        data.append(dict(type='scatter',
                         x=x, 
                         y=y, 
                         name='',
                         mode='lines', 
                         line=dict(width=size_diag[i]*arc_size, color='#6b8aca', shape='spline'),
                         hoverinfo='none'
                        )
                    )
        
    data.append(dict(type='scatter',
                        x=xx,
                        y=yy,
                        name='',
                        mode='markers',
                        marker=dict(size=0.5, color='#db2e2e'),
                        text=tooltips,
                        hoverinfo='text'))
    data.append(node_trace)
        
    title = " "
        
    layout = dict(
            title=title, 
            font=dict(size=10), 
            width=900,
            height=460,
            showlegend=False,
            xaxis=dict(anchor='y',
                    showline=False,  
                    zeroline=False,
                    showgrid=False,
                    tickvals=list(range(len(indices))), 
                    ticktext=indices,
                    tickangle=50,
                    ),
            yaxis=dict(visible=False), 
            hovermode='closest',
            margin=dict(t=80, b=110, l=10, r=10)    
            )
    fig = go.FigureWidget(data=data, layout=layout)
    fig.show()
