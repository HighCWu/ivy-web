import code
print(">>> import ivy_web")
import ivy_web
print(">>> ivy_web.__version__")
print(ivy_web.__version__)
print(">>> import ivy")
import ivy
print(">>> import ivy.functional.frontends.torch as torch")
import ivy.functional.frontends.torch as torch

print(">>> ivy.set_backend(\"numpy\")")
ivy.set_backend("numpy")

print(">>> torch.arange(10)")
print(torch.arange(10))

code.interact(banner="", local=locals())
