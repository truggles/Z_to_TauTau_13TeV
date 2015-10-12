import math

def compZeta( l1Pt, l1Phi, l2Pt, l2Phi, met, metPhi ) :

    l1x = math.cos(l1Phi)
    l1y = math.sin(l1Phi)
    l2x = math.cos(l2Phi)
    l2y = math.sin(l2Phi)

    zetaX = l1x + l2x
    zetaY = l1y + l2y
    zetaR = math.sqrt(zetaX*zetaX + zetaY*zetaY)
    if ( zetaR > 0. ) :
        zetaX /= zetaR
        zetaY /= zetaR

    visPx = l1Pt*l1x + l2Pt*l2x
    visPy = l1Pt*l1y + l2Pt*l2y
    pZetaVis = visPx*zetaX + visPy*zetaY

    px = visPx + met*( math.cos(metPhi) )
    py = visPy + met*( math.sin(metPhi) )
    pZeta = px*zetaX + py*zetaY
    
    if pZetaVis < 0 :
        print "\n ### Potential problem, pZetaVis = %f ###/n" % pZetaVis
    #//assert(pZetaVis >= 0.);

    return (pZetaVis, pZeta)

if __name__ == '__main__' :
    l1Pt = 100.
    l1Phi = 2.
    l2Pt = 150.
    l2Phi = -0.7
    met = 79.
    metPhi = 3.1416
    
    print compZeta( l1Pt, l1Phi, l2Pt, l2Phi, met, metPhi ) 
