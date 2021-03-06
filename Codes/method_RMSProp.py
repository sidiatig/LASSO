import numpy

from utils import errfun

def loss_func(A, x, b, mu):
    error = A.dot(x) - b
    loss = 1. / 2. * numpy.sum(error**2) + mu * numpy.sum(numpy.abs(x))
    return loss

def grad_func(A, x, b, mu):
    error = A.dot(x) - b
    grad_x = A.transpose().dot(error) + mu * numpy.sign(x)
    return grad_x

def init(n, x0):
    x = x0
    r = numpy.zeros((n, 1))
    return x, r

def iteration(A, x, b, r, mu, lr, delta, rho):
    grad_x = grad_func(A, x, b, mu)
    
    r = rho * r + (1. - rho) * grad_x * grad_x
    
    x = x - lr * grad_x / (delta + numpy.sqrt(r))
    
    return x, r, grad_x

def l1_sub_RMSProp(
    x0, A, b, mu,
    iter_list=[],
    lr_list=None,
    mu_list=None,
    rho_list=None,
    delta=None,
    res_list=None,
    sep=0, figure=False, xx=None, **opts
):
    m, n = A.shape
    
    mu0 = mu
    
    x, r = init(n, x0)
    
    t = 0
    iter_len = len(iter_list)
    
    formal_loss_list, real_loss_list, error_xx_list, grad_norm2_list = [], [], [], []
    
    for j in range(iter_len):
        lr = lr_list[j]
        mu = mu_list[j]
        rho = rho_list[j]
        
        for i in range(iter_list[j]):
            x, r, grad_x = iteration(A, x, b, r, mu, lr, delta, rho)
            
            if figure:
                formal_loss_list.append(loss_func(A, x, b, mu))
                real_loss_list.append(loss_func(A, x, b, mu0))
                if xx is not None:
                    error_xx_list.append(errfun(x, xx))
            
            if sep != 0 and t % sep == 0:
                loss = loss_func(A, x, b, mu0)
                print("i: {0}, j: {1}, t: {2}, loss: {3:.5e}".format(i, j, t, loss))
            
            if res_list is not None:
                grad_norm2 = numpy.sum(grad_x**2)
                if figure:
                    grad_norm2_list.append(grad_norm2)
                if grad_norm2 < res_list[j]:
                    break
                
            t += 1
    
    solution = x
    loss = loss_func(A, x, b, mu0)
    
    out = {
        "solution": solution,
        "loss": loss,
        "vars": 2*n,
        "iters": t,
        "conts": iter_len,
        "formal_loss": numpy.array(formal_loss_list),
        "real_loss": numpy.array(real_loss_list),
        "error": numpy.array(error_xx_list),
        "grad_norm2": numpy.array(grad_norm2_list),
    }
    
    return solution, out
