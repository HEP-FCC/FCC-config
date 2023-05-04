# This file was automatically created by FeynRules 2.3.12
# Mathematica version: 10.1.0  for Mac OS X x86 (64-bit) (March 24, 2015)
# Date: Thu 15 Oct 2015 14:28:46



from object_library import all_parameters, Parameter


from function_library import complexconjugate, re, im, csc, sec, acsc, asec, cot

# This is a default parameter object representing 0.
ZERO = Parameter(name = 'ZERO',
                 nature = 'internal',
                 type = 'real',
                 value = '0.0',
                 texname = '0')

# User-defined parameters.
cabi = Parameter(name = 'cabi',
                 nature = 'external',
                 type = 'real',
                 value = 0.227736,
                 texname = '\\theta _c',
                 lhablock = 'CKMBLOCK',
                 lhacode = [ 1 ])

l2 = Parameter(name = 'l2',
               nature = 'external',
               type = 'real',
               value = 0.5,
               texname = '\\lambda _2',
               lhablock = 'Higgs',
               lhacode = [ 1 ])

l3 = Parameter(name = 'l3',
               nature = 'external',
               type = 'real',
               value = 1,
               texname = '\\lambda _3',
               lhablock = 'Higgs',
               lhacode = [ 2 ])

lR7 = Parameter(name = 'lR7',
                nature = 'external',
                type = 'real',
                value = 0.1,
                texname = '\\text{lR7}',
                lhablock = 'Higgs',
                lhacode = [ 3 ])

lI7 = Parameter(name = 'lI7',
                nature = 'external',
                type = 'real',
                value = 0.2,
                texname = '\\text{lI7}',
                lhablock = 'Higgs',
                lhacode = [ 4 ])

mixh = Parameter(name = 'mixh',
                 nature = 'external',
                 type = 'real',
                 value = 0.3,
                 texname = '\\theta _{\\text{h1}}',
                 lhablock = 'Higgs',
                 lhacode = [ 5 ])

mixh2 = Parameter(name = 'mixh2',
                  nature = 'external',
                  type = 'real',
                  value = 0.1,
                  texname = '\\theta _{\\text{h2}}',
                  lhablock = 'Higgs',
                  lhacode = [ 6 ])

mixh3 = Parameter(name = 'mixh3',
                  nature = 'external',
                  type = 'real',
                  value = 0.2,
                  texname = '\\theta _{\\text{h3}}',
                  lhablock = 'Higgs',
                  lhacode = [ 7 ])

aEWM1 = Parameter(name = 'aEWM1',
                  nature = 'external',
                  type = 'real',
                  value = 127.9,
                  texname = '\\text{aEWM1}',
                  lhablock = 'SMINPUTS',
                  lhacode = [ 1 ])

Gf = Parameter(name = 'Gf',
               nature = 'external',
               type = 'real',
               value = 0.000011663900000000002,
               texname = '\\text{Gf}',
               lhablock = 'SMINPUTS',
               lhacode = [ 2 ])

aS = Parameter(name = 'aS',
               nature = 'external',
               type = 'real',
               value = 0.118,
               texname = '\\text{aS}',
               lhablock = 'SMINPUTS',
               lhacode = [ 3 ])

ymb = Parameter(name = 'ymb',
                nature = 'external',
                type = 'real',
                value = 4.7,
                texname = '\\text{ymb}',
                lhablock = 'YUKAWA',
                lhacode = [ 5 ])

ymt = Parameter(name = 'ymt',
                nature = 'external',
                type = 'real',
                value = 172,
                texname = '\\text{ymt}',
                lhablock = 'YUKAWA',
                lhacode = [ 6 ])

ymtau = Parameter(name = 'ymtau',
                  nature = 'external',
                  type = 'real',
                  value = 1.777,
                  texname = '\\text{ymtau}',
                  lhablock = 'YUKAWA',
                  lhacode = [ 15 ])

GDI1x1 = Parameter(name = 'GDI1x1',
                   nature = 'external',
                   type = 'real',
                   value = 0,
                   texname = '\\text{GDI1x1}',
                   lhablock = 'YukawaGDI',
                   lhacode = [ 1, 1 ])

GDI1x2 = Parameter(name = 'GDI1x2',
                   nature = 'external',
                   type = 'real',
                   value = 0,
                   texname = '\\text{GDI1x2}',
                   lhablock = 'YukawaGDI',
                   lhacode = [ 1, 2 ])

GDI1x3 = Parameter(name = 'GDI1x3',
                   nature = 'external',
                   type = 'real',
                   value = 0,
                   texname = '\\text{GDI1x3}',
                   lhablock = 'YukawaGDI',
                   lhacode = [ 1, 3 ])

GDI2x1 = Parameter(name = 'GDI2x1',
                   nature = 'external',
                   type = 'real',
                   value = 0,
                   texname = '\\text{GDI2x1}',
                   lhablock = 'YukawaGDI',
                   lhacode = [ 2, 1 ])

GDI2x2 = Parameter(name = 'GDI2x2',
                   nature = 'external',
                   type = 'real',
                   value = 0,
                   texname = '\\text{GDI2x2}',
                   lhablock = 'YukawaGDI',
                   lhacode = [ 2, 2 ])

GDI2x3 = Parameter(name = 'GDI2x3',
                   nature = 'external',
                   type = 'real',
                   value = 0,
                   texname = '\\text{GDI2x3}',
                   lhablock = 'YukawaGDI',
                   lhacode = [ 2, 3 ])

GDI3x1 = Parameter(name = 'GDI3x1',
                   nature = 'external',
                   type = 'real',
                   value = 0,
                   texname = '\\text{GDI3x1}',
                   lhablock = 'YukawaGDI',
                   lhacode = [ 3, 1 ])

GDI3x2 = Parameter(name = 'GDI3x2',
                   nature = 'external',
                   type = 'real',
                   value = 0,
                   texname = '\\text{GDI3x2}',
                   lhablock = 'YukawaGDI',
                   lhacode = [ 3, 2 ])

GDI3x3 = Parameter(name = 'GDI3x3',
                   nature = 'external',
                   type = 'real',
                   value = 0,
                   texname = '\\text{GDI3x3}',
                   lhablock = 'YukawaGDI',
                   lhacode = [ 3, 3 ])

GDR1x1 = Parameter(name = 'GDR1x1',
                   nature = 'external',
                   type = 'real',
                   value = 1,
                   texname = '\\text{GDR1x1}',
                   lhablock = 'YukawaGDR',
                   lhacode = [ 1, 1 ])

GDR1x2 = Parameter(name = 'GDR1x2',
                   nature = 'external',
                   type = 'real',
                   value = 0.01,
                   texname = '\\text{GDR1x2}',
                   lhablock = 'YukawaGDR',
                   lhacode = [ 1, 2 ])

GDR1x3 = Parameter(name = 'GDR1x3',
                   nature = 'external',
                   type = 'real',
                   value = 0.01,
                   texname = '\\text{GDR1x3}',
                   lhablock = 'YukawaGDR',
                   lhacode = [ 1, 3 ])

GDR2x1 = Parameter(name = 'GDR2x1',
                   nature = 'external',
                   type = 'real',
                   value = 0.01,
                   texname = '\\text{GDR2x1}',
                   lhablock = 'YukawaGDR',
                   lhacode = [ 2, 1 ])

GDR2x2 = Parameter(name = 'GDR2x2',
                   nature = 'external',
                   type = 'real',
                   value = 1,
                   texname = '\\text{GDR2x2}',
                   lhablock = 'YukawaGDR',
                   lhacode = [ 2, 2 ])

GDR2x3 = Parameter(name = 'GDR2x3',
                   nature = 'external',
                   type = 'real',
                   value = 0.01,
                   texname = '\\text{GDR2x3}',
                   lhablock = 'YukawaGDR',
                   lhacode = [ 2, 3 ])

GDR3x1 = Parameter(name = 'GDR3x1',
                   nature = 'external',
                   type = 'real',
                   value = 0.01,
                   texname = '\\text{GDR3x1}',
                   lhablock = 'YukawaGDR',
                   lhacode = [ 3, 1 ])

GDR3x2 = Parameter(name = 'GDR3x2',
                   nature = 'external',
                   type = 'real',
                   value = 0.01,
                   texname = '\\text{GDR3x2}',
                   lhablock = 'YukawaGDR',
                   lhacode = [ 3, 2 ])

GDR3x3 = Parameter(name = 'GDR3x3',
                   nature = 'external',
                   type = 'real',
                   value = 1,
                   texname = '\\text{GDR3x3}',
                   lhablock = 'YukawaGDR',
                   lhacode = [ 3, 3 ])

GLI1x1 = Parameter(name = 'GLI1x1',
                   nature = 'external',
                   type = 'real',
                   value = 0,
                   texname = '\\text{GLI1x1}',
                   lhablock = 'YukawaGLI',
                   lhacode = [ 1, 1 ])

GLI1x2 = Parameter(name = 'GLI1x2',
                   nature = 'external',
                   type = 'real',
                   value = 0,
                   texname = '\\text{GLI1x2}',
                   lhablock = 'YukawaGLI',
                   lhacode = [ 1, 2 ])

GLI1x3 = Parameter(name = 'GLI1x3',
                   nature = 'external',
                   type = 'real',
                   value = 0,
                   texname = '\\text{GLI1x3}',
                   lhablock = 'YukawaGLI',
                   lhacode = [ 1, 3 ])

GLI2x1 = Parameter(name = 'GLI2x1',
                   nature = 'external',
                   type = 'real',
                   value = 0,
                   texname = '\\text{GLI2x1}',
                   lhablock = 'YukawaGLI',
                   lhacode = [ 2, 1 ])

GLI2x2 = Parameter(name = 'GLI2x2',
                   nature = 'external',
                   type = 'real',
                   value = 0,
                   texname = '\\text{GLI2x2}',
                   lhablock = 'YukawaGLI',
                   lhacode = [ 2, 2 ])

GLI2x3 = Parameter(name = 'GLI2x3',
                   nature = 'external',
                   type = 'real',
                   value = 0,
                   texname = '\\text{GLI2x3}',
                   lhablock = 'YukawaGLI',
                   lhacode = [ 2, 3 ])

GLI3x1 = Parameter(name = 'GLI3x1',
                   nature = 'external',
                   type = 'real',
                   value = 0,
                   texname = '\\text{GLI3x1}',
                   lhablock = 'YukawaGLI',
                   lhacode = [ 3, 1 ])

GLI3x2 = Parameter(name = 'GLI3x2',
                   nature = 'external',
                   type = 'real',
                   value = 0,
                   texname = '\\text{GLI3x2}',
                   lhablock = 'YukawaGLI',
                   lhacode = [ 3, 2 ])

GLI3x3 = Parameter(name = 'GLI3x3',
                   nature = 'external',
                   type = 'real',
                   value = 0,
                   texname = '\\text{GLI3x3}',
                   lhablock = 'YukawaGLI',
                   lhacode = [ 3, 3 ])

GLR1x1 = Parameter(name = 'GLR1x1',
                   nature = 'external',
                   type = 'real',
                   value = 1,
                   texname = '\\text{GLR1x1}',
                   lhablock = 'YukawaGLR',
                   lhacode = [ 1, 1 ])

GLR1x2 = Parameter(name = 'GLR1x2',
                   nature = 'external',
                   type = 'real',
                   value = 0.01,
                   texname = '\\text{GLR1x2}',
                   lhablock = 'YukawaGLR',
                   lhacode = [ 1, 2 ])

GLR1x3 = Parameter(name = 'GLR1x3',
                   nature = 'external',
                   type = 'real',
                   value = 0.01,
                   texname = '\\text{GLR1x3}',
                   lhablock = 'YukawaGLR',
                   lhacode = [ 1, 3 ])

GLR2x1 = Parameter(name = 'GLR2x1',
                   nature = 'external',
                   type = 'real',
                   value = 0.01,
                   texname = '\\text{GLR2x1}',
                   lhablock = 'YukawaGLR',
                   lhacode = [ 2, 1 ])

GLR2x2 = Parameter(name = 'GLR2x2',
                   nature = 'external',
                   type = 'real',
                   value = 1,
                   texname = '\\text{GLR2x2}',
                   lhablock = 'YukawaGLR',
                   lhacode = [ 2, 2 ])

GLR2x3 = Parameter(name = 'GLR2x3',
                   nature = 'external',
                   type = 'real',
                   value = 0.01,
                   texname = '\\text{GLR2x3}',
                   lhablock = 'YukawaGLR',
                   lhacode = [ 2, 3 ])

GLR3x1 = Parameter(name = 'GLR3x1',
                   nature = 'external',
                   type = 'real',
                   value = 0.01,
                   texname = '\\text{GLR3x1}',
                   lhablock = 'YukawaGLR',
                   lhacode = [ 3, 1 ])

GLR3x2 = Parameter(name = 'GLR3x2',
                   nature = 'external',
                   type = 'real',
                   value = 0.01,
                   texname = '\\text{GLR3x2}',
                   lhablock = 'YukawaGLR',
                   lhacode = [ 3, 2 ])

GLR3x3 = Parameter(name = 'GLR3x3',
                   nature = 'external',
                   type = 'real',
                   value = 1,
                   texname = '\\text{GLR3x3}',
                   lhablock = 'YukawaGLR',
                   lhacode = [ 3, 3 ])

GUI1x1 = Parameter(name = 'GUI1x1',
                   nature = 'external',
                   type = 'real',
                   value = 0,
                   texname = '\\text{GUI1x1}',
                   lhablock = 'YukawaGUI',
                   lhacode = [ 1, 1 ])

GUI1x2 = Parameter(name = 'GUI1x2',
                   nature = 'external',
                   type = 'real',
                   value = 0,
                   texname = '\\text{GUI1x2}',
                   lhablock = 'YukawaGUI',
                   lhacode = [ 1, 2 ])

GUI1x3 = Parameter(name = 'GUI1x3',
                   nature = 'external',
                   type = 'real',
                   value = 0,
                   texname = '\\text{GUI1x3}',
                   lhablock = 'YukawaGUI',
                   lhacode = [ 1, 3 ])

GUI2x1 = Parameter(name = 'GUI2x1',
                   nature = 'external',
                   type = 'real',
                   value = 0,
                   texname = '\\text{GUI2x1}',
                   lhablock = 'YukawaGUI',
                   lhacode = [ 2, 1 ])

GUI2x2 = Parameter(name = 'GUI2x2',
                   nature = 'external',
                   type = 'real',
                   value = 0,
                   texname = '\\text{GUI2x2}',
                   lhablock = 'YukawaGUI',
                   lhacode = [ 2, 2 ])

GUI2x3 = Parameter(name = 'GUI2x3',
                   nature = 'external',
                   type = 'real',
                   value = 0,
                   texname = '\\text{GUI2x3}',
                   lhablock = 'YukawaGUI',
                   lhacode = [ 2, 3 ])

GUI3x1 = Parameter(name = 'GUI3x1',
                   nature = 'external',
                   type = 'real',
                   value = 0,
                   texname = '\\text{GUI3x1}',
                   lhablock = 'YukawaGUI',
                   lhacode = [ 3, 1 ])

GUI3x2 = Parameter(name = 'GUI3x2',
                   nature = 'external',
                   type = 'real',
                   value = 0,
                   texname = '\\text{GUI3x2}',
                   lhablock = 'YukawaGUI',
                   lhacode = [ 3, 2 ])

GUI3x3 = Parameter(name = 'GUI3x3',
                   nature = 'external',
                   type = 'real',
                   value = 0,
                   texname = '\\text{GUI3x3}',
                   lhablock = 'YukawaGUI',
                   lhacode = [ 3, 3 ])

GUR1x1 = Parameter(name = 'GUR1x1',
                   nature = 'external',
                   type = 'real',
                   value = 1,
                   texname = '\\text{GUR1x1}',
                   lhablock = 'YukawaGUR',
                   lhacode = [ 1, 1 ])

GUR1x2 = Parameter(name = 'GUR1x2',
                   nature = 'external',
                   type = 'real',
                   value = 0.01,
                   texname = '\\text{GUR1x2}',
                   lhablock = 'YukawaGUR',
                   lhacode = [ 1, 2 ])

GUR1x3 = Parameter(name = 'GUR1x3',
                   nature = 'external',
                   type = 'real',
                   value = 0.01,
                   texname = '\\text{GUR1x3}',
                   lhablock = 'YukawaGUR',
                   lhacode = [ 1, 3 ])

GUR2x1 = Parameter(name = 'GUR2x1',
                   nature = 'external',
                   type = 'real',
                   value = 0.01,
                   texname = '\\text{GUR2x1}',
                   lhablock = 'YukawaGUR',
                   lhacode = [ 2, 1 ])

GUR2x2 = Parameter(name = 'GUR2x2',
                   nature = 'external',
                   type = 'real',
                   value = 1,
                   texname = '\\text{GUR2x2}',
                   lhablock = 'YukawaGUR',
                   lhacode = [ 2, 2 ])

GUR2x3 = Parameter(name = 'GUR2x3',
                   nature = 'external',
                   type = 'real',
                   value = 0.01,
                   texname = '\\text{GUR2x3}',
                   lhablock = 'YukawaGUR',
                   lhacode = [ 2, 3 ])

GUR3x1 = Parameter(name = 'GUR3x1',
                   nature = 'external',
                   type = 'real',
                   value = 0.01,
                   texname = '\\text{GUR3x1}',
                   lhablock = 'YukawaGUR',
                   lhacode = [ 3, 1 ])

GUR3x2 = Parameter(name = 'GUR3x2',
                   nature = 'external',
                   type = 'real',
                   value = 0.01,
                   texname = '\\text{GUR3x2}',
                   lhablock = 'YukawaGUR',
                   lhacode = [ 3, 2 ])

GUR3x3 = Parameter(name = 'GUR3x3',
                   nature = 'external',
                   type = 'real',
                   value = 1,
                   texname = '\\text{GUR3x3}',
                   lhablock = 'YukawaGUR',
                   lhacode = [ 3, 3 ])

MZ = Parameter(name = 'MZ',
               nature = 'external',
               type = 'real',
               value = 91.1876,
               texname = '\\text{MZ}',
               lhablock = 'MASS',
               lhacode = [ 23 ])

MT = Parameter(name = 'MT',
               nature = 'external',
               type = 'real',
               value = 172,
               texname = '\\text{MT}',
               lhablock = 'MASS',
               lhacode = [ 6 ])

MB = Parameter(name = 'MB',
               nature = 'external',
               type = 'real',
               value = 4.7,
               texname = '\\text{MB}',
               lhablock = 'MASS',
               lhacode = [ 5 ])

mhc = Parameter(name = 'mhc',
                nature = 'external',
                type = 'real',
                value = 150,
                texname = '\\text{mhc}',
                lhablock = 'MASS',
                lhacode = [ 37 ])

mh1 = Parameter(name = 'mh1',
                nature = 'external',
                type = 'real',
                value = 125,
                texname = '\\text{mh1}',
                lhablock = 'MASS',
                lhacode = [ 25 ])

mh2 = Parameter(name = 'mh2',
                nature = 'external',
                type = 'real',
                value = 130,
                texname = '\\text{mh2}',
                lhablock = 'MASS',
                lhacode = [ 35 ])

mh3 = Parameter(name = 'mh3',
                nature = 'external',
                type = 'real',
                value = 140,
                texname = '\\text{mh3}',
                lhablock = 'MASS',
                lhacode = [ 36 ])

WZ = Parameter(name = 'WZ',
               nature = 'external',
               type = 'real',
               value = 2.4952,
               texname = '\\text{WZ}',
               lhablock = 'DECAY',
               lhacode = [ 23 ])

WW = Parameter(name = 'WW',
               nature = 'external',
               type = 'real',
               value = 2.085,
               texname = '\\text{WW}',
               lhablock = 'DECAY',
               lhacode = [ 24 ])

WT = Parameter(name = 'WT',
               nature = 'external',
               type = 'real',
               value = 1.50833649,
               texname = '\\text{WT}',
               lhablock = 'DECAY',
               lhacode = [ 6 ])

whc = Parameter(name = 'whc',
                nature = 'external',
                type = 'real',
                value = 1,
                texname = '\\text{whc}',
                lhablock = 'DECAY',
                lhacode = [ 37 ])

Wh1 = Parameter(name = 'Wh1',
                nature = 'external',
                type = 'real',
                value = 1,
                texname = '\\text{Wh1}',
                lhablock = 'DECAY',
                lhacode = [ 25 ])

Wh2 = Parameter(name = 'Wh2',
                nature = 'external',
                type = 'real',
                value = 1,
                texname = '\\text{Wh2}',
                lhablock = 'DECAY',
                lhacode = [ 35 ])

Wh3 = Parameter(name = 'Wh3',
                nature = 'external',
                type = 'real',
                value = 1,
                texname = '\\text{Wh3}',
                lhablock = 'DECAY',
                lhacode = [ 36 ])

CKM1x1 = Parameter(name = 'CKM1x1',
                   nature = 'internal',
                   type = 'complex',
                   value = 'cmath.cos(cabi)',
                   texname = '\\text{CKM1x1}')

CKM1x2 = Parameter(name = 'CKM1x2',
                   nature = 'internal',
                   type = 'complex',
                   value = 'cmath.sin(cabi)',
                   texname = '\\text{CKM1x2}')

CKM1x3 = Parameter(name = 'CKM1x3',
                   nature = 'internal',
                   type = 'complex',
                   value = '0',
                   texname = '\\text{CKM1x3}')

CKM2x1 = Parameter(name = 'CKM2x1',
                   nature = 'internal',
                   type = 'complex',
                   value = '-cmath.sin(cabi)',
                   texname = '\\text{CKM2x1}')

CKM2x2 = Parameter(name = 'CKM2x2',
                   nature = 'internal',
                   type = 'complex',
                   value = 'cmath.cos(cabi)',
                   texname = '\\text{CKM2x2}')

CKM2x3 = Parameter(name = 'CKM2x3',
                   nature = 'internal',
                   type = 'complex',
                   value = '0',
                   texname = '\\text{CKM2x3}')

CKM3x1 = Parameter(name = 'CKM3x1',
                   nature = 'internal',
                   type = 'complex',
                   value = '0',
                   texname = '\\text{CKM3x1}')

CKM3x2 = Parameter(name = 'CKM3x2',
                   nature = 'internal',
                   type = 'complex',
                   value = '0',
                   texname = '\\text{CKM3x2}')

CKM3x3 = Parameter(name = 'CKM3x3',
                   nature = 'internal',
                   type = 'complex',
                   value = '1',
                   texname = '\\text{CKM3x3}')

TH1x1 = Parameter(name = 'TH1x1',
                  nature = 'internal',
                  type = 'real',
                  value = 'cmath.cos(mixh)*cmath.cos(mixh2)',
                  texname = '\\text{TH1x1}')

TH1x2 = Parameter(name = 'TH1x2',
                  nature = 'internal',
                  type = 'real',
                  value = 'cmath.cos(mixh2)*cmath.sin(mixh)',
                  texname = '\\text{TH1x2}')

TH1x3 = Parameter(name = 'TH1x3',
                  nature = 'internal',
                  type = 'real',
                  value = '-cmath.sin(mixh2)',
                  texname = '\\text{TH1x3}')

TH2x1 = Parameter(name = 'TH2x1',
                  nature = 'internal',
                  type = 'real',
                  value = '-(cmath.cos(mixh3)*cmath.sin(mixh)) + cmath.cos(mixh)*cmath.sin(mixh2)*cmath.sin(mixh3)',
                  texname = '\\text{TH2x1}')

TH2x2 = Parameter(name = 'TH2x2',
                  nature = 'internal',
                  type = 'real',
                  value = 'cmath.cos(mixh)*cmath.cos(mixh3) + cmath.sin(mixh)*cmath.sin(mixh2)*cmath.sin(mixh3)',
                  texname = '\\text{TH2x2}')

TH2x3 = Parameter(name = 'TH2x3',
                  nature = 'internal',
                  type = 'real',
                  value = 'cmath.cos(mixh2)*cmath.sin(mixh3)',
                  texname = '\\text{TH2x3}')

TH3x1 = Parameter(name = 'TH3x1',
                  nature = 'internal',
                  type = 'real',
                  value = 'cmath.cos(mixh)*cmath.cos(mixh3)*cmath.sin(mixh2) + cmath.sin(mixh)*cmath.sin(mixh3)',
                  texname = '\\text{TH3x1}')

TH3x2 = Parameter(name = 'TH3x2',
                  nature = 'internal',
                  type = 'real',
                  value = 'cmath.cos(mixh3)*cmath.sin(mixh)*cmath.sin(mixh2) - cmath.cos(mixh)*cmath.sin(mixh3)',
                  texname = '\\text{TH3x2}')

TH3x3 = Parameter(name = 'TH3x3',
                  nature = 'internal',
                  type = 'real',
                  value = 'cmath.cos(mixh2)*cmath.cos(mixh3)',
                  texname = '\\text{TH3x3}')

aEW = Parameter(name = 'aEW',
                nature = 'internal',
                type = 'real',
                value = '1/aEWM1',
                texname = '\\text{aEW}')

G = Parameter(name = 'G',
              nature = 'internal',
              type = 'real',
              value = '2*cmath.sqrt(aS)*cmath.sqrt(cmath.pi)',
              texname = 'G')

GD1x1 = Parameter(name = 'GD1x1',
                  nature = 'internal',
                  type = 'complex',
                  value = 'complex(0,1)*GDI1x1 + GDR1x1',
                  texname = '\\text{GD1x1}')

GD1x2 = Parameter(name = 'GD1x2',
                  nature = 'internal',
                  type = 'complex',
                  value = 'complex(0,1)*GDI1x2 + GDR1x2',
                  texname = '\\text{GD1x2}')

GD1x3 = Parameter(name = 'GD1x3',
                  nature = 'internal',
                  type = 'complex',
                  value = 'complex(0,1)*GDI1x3 + GDR1x3',
                  texname = '\\text{GD1x3}')

GD2x1 = Parameter(name = 'GD2x1',
                  nature = 'internal',
                  type = 'complex',
                  value = 'complex(0,1)*GDI2x1 + GDR2x1',
                  texname = '\\text{GD2x1}')

GD2x2 = Parameter(name = 'GD2x2',
                  nature = 'internal',
                  type = 'complex',
                  value = 'complex(0,1)*GDI2x2 + GDR2x2',
                  texname = '\\text{GD2x2}')

GD2x3 = Parameter(name = 'GD2x3',
                  nature = 'internal',
                  type = 'complex',
                  value = 'complex(0,1)*GDI2x3 + GDR2x3',
                  texname = '\\text{GD2x3}')

GD3x1 = Parameter(name = 'GD3x1',
                  nature = 'internal',
                  type = 'complex',
                  value = 'complex(0,1)*GDI3x1 + GDR3x1',
                  texname = '\\text{GD3x1}')

GD3x2 = Parameter(name = 'GD3x2',
                  nature = 'internal',
                  type = 'complex',
                  value = 'complex(0,1)*GDI3x2 + GDR3x2',
                  texname = '\\text{GD3x2}')

GD3x3 = Parameter(name = 'GD3x3',
                  nature = 'internal',
                  type = 'complex',
                  value = 'complex(0,1)*GDI3x3 + GDR3x3',
                  texname = '\\text{GD3x3}')

GL1x1 = Parameter(name = 'GL1x1',
                  nature = 'internal',
                  type = 'complex',
                  value = 'complex(0,1)*GLI1x1 + GLR1x1',
                  texname = '\\text{GL1x1}')

GL1x2 = Parameter(name = 'GL1x2',
                  nature = 'internal',
                  type = 'complex',
                  value = 'complex(0,1)*GLI1x2 + GLR1x2',
                  texname = '\\text{GL1x2}')

GL1x3 = Parameter(name = 'GL1x3',
                  nature = 'internal',
                  type = 'complex',
                  value = 'complex(0,1)*GLI1x3 + GLR1x3',
                  texname = '\\text{GL1x3}')

GL2x1 = Parameter(name = 'GL2x1',
                  nature = 'internal',
                  type = 'complex',
                  value = 'complex(0,1)*GLI2x1 + GLR2x1',
                  texname = '\\text{GL2x1}')

GL2x2 = Parameter(name = 'GL2x2',
                  nature = 'internal',
                  type = 'complex',
                  value = 'complex(0,1)*GLI2x2 + GLR2x2',
                  texname = '\\text{GL2x2}')

GL2x3 = Parameter(name = 'GL2x3',
                  nature = 'internal',
                  type = 'complex',
                  value = 'complex(0,1)*GLI2x3 + GLR2x3',
                  texname = '\\text{GL2x3}')

GL3x1 = Parameter(name = 'GL3x1',
                  nature = 'internal',
                  type = 'complex',
                  value = 'complex(0,1)*GLI3x1 + GLR3x1',
                  texname = '\\text{GL3x1}')

GL3x2 = Parameter(name = 'GL3x2',
                  nature = 'internal',
                  type = 'complex',
                  value = 'complex(0,1)*GLI3x2 + GLR3x2',
                  texname = '\\text{GL3x2}')

GL3x3 = Parameter(name = 'GL3x3',
                  nature = 'internal',
                  type = 'complex',
                  value = 'complex(0,1)*GLI3x3 + GLR3x3',
                  texname = '\\text{GL3x3}')

GU1x1 = Parameter(name = 'GU1x1',
                  nature = 'internal',
                  type = 'complex',
                  value = 'complex(0,1)*GUI1x1 + GUR1x1',
                  texname = '\\text{GU1x1}')

GU1x2 = Parameter(name = 'GU1x2',
                  nature = 'internal',
                  type = 'complex',
                  value = 'complex(0,1)*GUI1x2 + GUR1x2',
                  texname = '\\text{GU1x2}')

GU1x3 = Parameter(name = 'GU1x3',
                  nature = 'internal',
                  type = 'complex',
                  value = 'complex(0,1)*GUI1x3 + GUR1x3',
                  texname = '\\text{GU1x3}')

GU2x1 = Parameter(name = 'GU2x1',
                  nature = 'internal',
                  type = 'complex',
                  value = 'complex(0,1)*GUI2x1 + GUR2x1',
                  texname = '\\text{GU2x1}')

GU2x2 = Parameter(name = 'GU2x2',
                  nature = 'internal',
                  type = 'complex',
                  value = 'complex(0,1)*GUI2x2 + GUR2x2',
                  texname = '\\text{GU2x2}')

GU2x3 = Parameter(name = 'GU2x3',
                  nature = 'internal',
                  type = 'complex',
                  value = 'complex(0,1)*GUI2x3 + GUR2x3',
                  texname = '\\text{GU2x3}')

GU3x1 = Parameter(name = 'GU3x1',
                  nature = 'internal',
                  type = 'complex',
                  value = 'complex(0,1)*GUI3x1 + GUR3x1',
                  texname = '\\text{GU3x1}')

GU3x2 = Parameter(name = 'GU3x2',
                  nature = 'internal',
                  type = 'complex',
                  value = 'complex(0,1)*GUI3x2 + GUR3x2',
                  texname = '\\text{GU3x2}')

GU3x3 = Parameter(name = 'GU3x3',
                  nature = 'internal',
                  type = 'complex',
                  value = 'complex(0,1)*GUI3x3 + GUR3x3',
                  texname = '\\text{GU3x3}')

l7 = Parameter(name = 'l7',
               nature = 'internal',
               type = 'complex',
               value = 'complex(0,1)*lI7 + lR7',
               texname = '\\lambda _7')

MW = Parameter(name = 'MW',
               nature = 'internal',
               type = 'real',
               value = 'cmath.sqrt(MZ**2/2. + cmath.sqrt(MZ**4/4. - (aEW*cmath.pi*MZ**2)/(Gf*cmath.sqrt(2))))',
               texname = '\\text{MW}')

ee = Parameter(name = 'ee',
               nature = 'internal',
               type = 'real',
               value = '2*cmath.sqrt(aEW)*cmath.sqrt(cmath.pi)',
               texname = 'e')

sw2 = Parameter(name = 'sw2',
                nature = 'internal',
                type = 'real',
                value = '1 - MW**2/MZ**2',
                texname = '\\text{sw2}')

cw = Parameter(name = 'cw',
               nature = 'internal',
               type = 'real',
               value = 'cmath.sqrt(1 - sw2)',
               texname = 'c_w')

sw = Parameter(name = 'sw',
               nature = 'internal',
               type = 'real',
               value = 'cmath.sqrt(sw2)',
               texname = 's_w')

g1 = Parameter(name = 'g1',
               nature = 'internal',
               type = 'real',
               value = 'ee/cw',
               texname = 'g_1')

gw = Parameter(name = 'gw',
               nature = 'internal',
               type = 'real',
               value = 'ee/sw',
               texname = 'g_w')

vev = Parameter(name = 'vev',
                nature = 'internal',
                type = 'real',
                value = '(2*MW*sw)/ee',
                texname = '\\text{vev}')

mu2 = Parameter(name = 'mu2',
                nature = 'internal',
                type = 'real',
                value = 'mhc**2 - (l3*vev**2)/2.',
                texname = '\\text{mu2}')

l1 = Parameter(name = 'l1',
               nature = 'internal',
               type = 'real',
               value = '-(-(mh1**2*cmath.cos(mixh)**2*cmath.cos(mixh2)**2) - mh2**2*cmath.cos(mixh2)**2*cmath.sin(mixh)**2 - mh3**2*cmath.sin(mixh2)**2)/(2.*vev**2)',
               texname = '\\lambda _1')

l4 = Parameter(name = 'l4',
               nature = 'internal',
               type = 'real',
               value = '(3*mh1**2 + 3*mh2**2 + 2*mh3**2 - 8*mhc**2 + 2*(-mh1**2 + mh2**2)*cmath.cos(2*mixh)*cmath.cos(mixh2)**2 - (mh1**2 + mh2**2 - 2*mh3**2)*cmath.cos(2*mixh2))/(4.*vev**2)',
               texname = '\\lambda _4')

lI5 = Parameter(name = 'lI5',
                nature = 'internal',
                type = 'real',
                value = '((mh1 - mh2)*(mh1 + mh2)*cmath.cos(mixh)*cmath.cos(2*mixh3)*cmath.sin(mixh)*cmath.sin(mixh2) + cmath.cos(mixh3)*(-(mh3**2*cmath.cos(mixh2)**2) + cmath.cos(mixh)**2*(mh2**2 - mh1**2*cmath.sin(mixh2)**2) + cmath.sin(mixh)**2*(mh1**2 - mh2**2*cmath.sin(mixh2)**2))*cmath.sin(mixh3))/vev**2',
                texname = '\\text{lI5}')

lI6 = Parameter(name = 'lI6',
                nature = 'internal',
                type = 'real',
                value = '(cmath.cos(mixh2)*(cmath.cos(mixh3)*(mh3**2 - mh1**2*cmath.cos(mixh)**2 - mh2**2*cmath.sin(mixh)**2)*cmath.sin(mixh2) + (-mh1**2 + mh2**2)*cmath.cos(mixh)*cmath.sin(mixh)*cmath.sin(mixh3)))/vev**2',
                texname = '\\text{lI6}')

lR5 = Parameter(name = 'lR5',
                nature = 'internal',
                type = 'real',
                value = '((2*(mh1**2 + mh2**2 - 2*mh3**2)*cmath.cos(mixh2)**2 + (mh1 - mh2)*(mh1 + mh2)*cmath.cos(2*mixh)*(-3 + cmath.cos(2*mixh2)))*cmath.cos(2*mixh3) + 4*(-mh1**2 + mh2**2)*cmath.sin(2*mixh)*cmath.sin(mixh2)*cmath.sin(2*mixh3))/(8.*vev**2)',
                texname = '\\text{lR5}')

lR6 = Parameter(name = 'lR6',
                nature = 'internal',
                type = 'real',
                value = '(cmath.cos(mixh2)*((-mh1**2 + mh2**2)*cmath.cos(mixh)*cmath.cos(mixh3)*cmath.sin(mixh) + (-mh3**2 + mh1**2*cmath.cos(mixh)**2 + mh2**2*cmath.sin(mixh)**2)*cmath.sin(mixh2)*cmath.sin(mixh3)))/vev**2',
                texname = '\\text{lR6}')

yb = Parameter(name = 'yb',
               nature = 'internal',
               type = 'real',
               value = '(ymb*cmath.sqrt(2))/vev',
               texname = '\\text{yb}')

yt = Parameter(name = 'yt',
               nature = 'internal',
               type = 'real',
               value = '(ymt*cmath.sqrt(2))/vev',
               texname = '\\text{yt}')

ytau = Parameter(name = 'ytau',
                 nature = 'internal',
                 type = 'real',
                 value = '(ymtau*cmath.sqrt(2))/vev',
                 texname = '\\text{ytau}')

mu1 = Parameter(name = 'mu1',
                nature = 'internal',
                type = 'real',
                value = '-(l1*vev**2)',
                texname = '\\text{mu1}')

l5 = Parameter(name = 'l5',
               nature = 'internal',
               type = 'complex',
               value = 'complex(0,1)*lI5 + lR5',
               texname = '\\lambda _5')

l6 = Parameter(name = 'l6',
               nature = 'internal',
               type = 'complex',
               value = 'complex(0,1)*lI6 + lR6',
               texname = '\\lambda _6')

mu3 = Parameter(name = 'mu3',
                nature = 'internal',
                type = 'complex',
                value = '-(l6*vev**2)/2.',
                texname = '\\text{mu3}')

I1a11 = Parameter(name = 'I1a11',
                  nature = 'internal',
                  type = 'complex',
                  value = 'complexconjugate(CKM1x1)*complexconjugate(GD1x1) + complexconjugate(CKM1x2)*complexconjugate(GD2x1) + complexconjugate(CKM1x3)*complexconjugate(GD3x1)',
                  texname = '\\text{I1a11}')

I1a12 = Parameter(name = 'I1a12',
                  nature = 'internal',
                  type = 'complex',
                  value = 'complexconjugate(CKM2x1)*complexconjugate(GD1x1) + complexconjugate(CKM2x2)*complexconjugate(GD2x1) + complexconjugate(CKM2x3)*complexconjugate(GD3x1)',
                  texname = '\\text{I1a12}')

I1a13 = Parameter(name = 'I1a13',
                  nature = 'internal',
                  type = 'complex',
                  value = 'complexconjugate(CKM3x1)*complexconjugate(GD1x1) + complexconjugate(CKM3x2)*complexconjugate(GD2x1) + complexconjugate(CKM3x3)*complexconjugate(GD3x1)',
                  texname = '\\text{I1a13}')

I1a21 = Parameter(name = 'I1a21',
                  nature = 'internal',
                  type = 'complex',
                  value = 'complexconjugate(CKM1x1)*complexconjugate(GD1x2) + complexconjugate(CKM1x2)*complexconjugate(GD2x2) + complexconjugate(CKM1x3)*complexconjugate(GD3x2)',
                  texname = '\\text{I1a21}')

I1a22 = Parameter(name = 'I1a22',
                  nature = 'internal',
                  type = 'complex',
                  value = 'complexconjugate(CKM2x1)*complexconjugate(GD1x2) + complexconjugate(CKM2x2)*complexconjugate(GD2x2) + complexconjugate(CKM2x3)*complexconjugate(GD3x2)',
                  texname = '\\text{I1a22}')

I1a23 = Parameter(name = 'I1a23',
                  nature = 'internal',
                  type = 'complex',
                  value = 'complexconjugate(CKM3x1)*complexconjugate(GD1x2) + complexconjugate(CKM3x2)*complexconjugate(GD2x2) + complexconjugate(CKM3x3)*complexconjugate(GD3x2)',
                  texname = '\\text{I1a23}')

I1a31 = Parameter(name = 'I1a31',
                  nature = 'internal',
                  type = 'complex',
                  value = 'complexconjugate(CKM1x1)*complexconjugate(GD1x3) + complexconjugate(CKM1x2)*complexconjugate(GD2x3) + complexconjugate(CKM1x3)*complexconjugate(GD3x3)',
                  texname = '\\text{I1a31}')

I1a32 = Parameter(name = 'I1a32',
                  nature = 'internal',
                  type = 'complex',
                  value = 'complexconjugate(CKM2x1)*complexconjugate(GD1x3) + complexconjugate(CKM2x2)*complexconjugate(GD2x3) + complexconjugate(CKM2x3)*complexconjugate(GD3x3)',
                  texname = '\\text{I1a32}')

I1a33 = Parameter(name = 'I1a33',
                  nature = 'internal',
                  type = 'complex',
                  value = 'complexconjugate(CKM3x1)*complexconjugate(GD1x3) + complexconjugate(CKM3x2)*complexconjugate(GD2x3) + complexconjugate(CKM3x3)*complexconjugate(GD3x3)',
                  texname = '\\text{I1a33}')

I2a11 = Parameter(name = 'I2a11',
                  nature = 'internal',
                  type = 'complex',
                  value = 'GU1x1*complexconjugate(CKM1x1) + GU2x1*complexconjugate(CKM2x1) + GU3x1*complexconjugate(CKM3x1)',
                  texname = '\\text{I2a11}')

I2a12 = Parameter(name = 'I2a12',
                  nature = 'internal',
                  type = 'complex',
                  value = 'GU1x2*complexconjugate(CKM1x1) + GU2x2*complexconjugate(CKM2x1) + GU3x2*complexconjugate(CKM3x1)',
                  texname = '\\text{I2a12}')

I2a13 = Parameter(name = 'I2a13',
                  nature = 'internal',
                  type = 'complex',
                  value = 'GU1x3*complexconjugate(CKM1x1) + GU2x3*complexconjugate(CKM2x1) + GU3x3*complexconjugate(CKM3x1)',
                  texname = '\\text{I2a13}')

I2a21 = Parameter(name = 'I2a21',
                  nature = 'internal',
                  type = 'complex',
                  value = 'GU1x1*complexconjugate(CKM1x2) + GU2x1*complexconjugate(CKM2x2) + GU3x1*complexconjugate(CKM3x2)',
                  texname = '\\text{I2a21}')

I2a22 = Parameter(name = 'I2a22',
                  nature = 'internal',
                  type = 'complex',
                  value = 'GU1x2*complexconjugate(CKM1x2) + GU2x2*complexconjugate(CKM2x2) + GU3x2*complexconjugate(CKM3x2)',
                  texname = '\\text{I2a22}')

I2a23 = Parameter(name = 'I2a23',
                  nature = 'internal',
                  type = 'complex',
                  value = 'GU1x3*complexconjugate(CKM1x2) + GU2x3*complexconjugate(CKM2x2) + GU3x3*complexconjugate(CKM3x2)',
                  texname = '\\text{I2a23}')

I2a31 = Parameter(name = 'I2a31',
                  nature = 'internal',
                  type = 'complex',
                  value = 'GU1x1*complexconjugate(CKM1x3) + GU2x1*complexconjugate(CKM2x3) + GU3x1*complexconjugate(CKM3x3)',
                  texname = '\\text{I2a31}')

I2a32 = Parameter(name = 'I2a32',
                  nature = 'internal',
                  type = 'complex',
                  value = 'GU1x2*complexconjugate(CKM1x3) + GU2x2*complexconjugate(CKM2x3) + GU3x2*complexconjugate(CKM3x3)',
                  texname = '\\text{I2a32}')

I2a33 = Parameter(name = 'I2a33',
                  nature = 'internal',
                  type = 'complex',
                  value = 'GU1x3*complexconjugate(CKM1x3) + GU2x3*complexconjugate(CKM2x3) + GU3x3*complexconjugate(CKM3x3)',
                  texname = '\\text{I2a33}')

I3a11 = Parameter(name = 'I3a11',
                  nature = 'internal',
                  type = 'complex',
                  value = 'CKM1x1*complexconjugate(GU1x1) + CKM2x1*complexconjugate(GU2x1) + CKM3x1*complexconjugate(GU3x1)',
                  texname = '\\text{I3a11}')

I3a12 = Parameter(name = 'I3a12',
                  nature = 'internal',
                  type = 'complex',
                  value = 'CKM1x2*complexconjugate(GU1x1) + CKM2x2*complexconjugate(GU2x1) + CKM3x2*complexconjugate(GU3x1)',
                  texname = '\\text{I3a12}')

I3a13 = Parameter(name = 'I3a13',
                  nature = 'internal',
                  type = 'complex',
                  value = 'CKM1x3*complexconjugate(GU1x1) + CKM2x3*complexconjugate(GU2x1) + CKM3x3*complexconjugate(GU3x1)',
                  texname = '\\text{I3a13}')

I3a21 = Parameter(name = 'I3a21',
                  nature = 'internal',
                  type = 'complex',
                  value = 'CKM1x1*complexconjugate(GU1x2) + CKM2x1*complexconjugate(GU2x2) + CKM3x1*complexconjugate(GU3x2)',
                  texname = '\\text{I3a21}')

I3a22 = Parameter(name = 'I3a22',
                  nature = 'internal',
                  type = 'complex',
                  value = 'CKM1x2*complexconjugate(GU1x2) + CKM2x2*complexconjugate(GU2x2) + CKM3x2*complexconjugate(GU3x2)',
                  texname = '\\text{I3a22}')

I3a23 = Parameter(name = 'I3a23',
                  nature = 'internal',
                  type = 'complex',
                  value = 'CKM1x3*complexconjugate(GU1x2) + CKM2x3*complexconjugate(GU2x2) + CKM3x3*complexconjugate(GU3x2)',
                  texname = '\\text{I3a23}')

I3a31 = Parameter(name = 'I3a31',
                  nature = 'internal',
                  type = 'complex',
                  value = 'CKM1x1*complexconjugate(GU1x3) + CKM2x1*complexconjugate(GU2x3) + CKM3x1*complexconjugate(GU3x3)',
                  texname = '\\text{I3a31}')

I3a32 = Parameter(name = 'I3a32',
                  nature = 'internal',
                  type = 'complex',
                  value = 'CKM1x2*complexconjugate(GU1x3) + CKM2x2*complexconjugate(GU2x3) + CKM3x2*complexconjugate(GU3x3)',
                  texname = '\\text{I3a32}')

I3a33 = Parameter(name = 'I3a33',
                  nature = 'internal',
                  type = 'complex',
                  value = 'CKM1x3*complexconjugate(GU1x3) + CKM2x3*complexconjugate(GU2x3) + CKM3x3*complexconjugate(GU3x3)',
                  texname = '\\text{I3a33}')

I4a11 = Parameter(name = 'I4a11',
                  nature = 'internal',
                  type = 'complex',
                  value = 'CKM1x1*GD1x1 + CKM1x2*GD2x1 + CKM1x3*GD3x1',
                  texname = '\\text{I4a11}')

I4a12 = Parameter(name = 'I4a12',
                  nature = 'internal',
                  type = 'complex',
                  value = 'CKM1x1*GD1x2 + CKM1x2*GD2x2 + CKM1x3*GD3x2',
                  texname = '\\text{I4a12}')

I4a13 = Parameter(name = 'I4a13',
                  nature = 'internal',
                  type = 'complex',
                  value = 'CKM1x1*GD1x3 + CKM1x2*GD2x3 + CKM1x3*GD3x3',
                  texname = '\\text{I4a13}')

I4a21 = Parameter(name = 'I4a21',
                  nature = 'internal',
                  type = 'complex',
                  value = 'CKM2x1*GD1x1 + CKM2x2*GD2x1 + CKM2x3*GD3x1',
                  texname = '\\text{I4a21}')

I4a22 = Parameter(name = 'I4a22',
                  nature = 'internal',
                  type = 'complex',
                  value = 'CKM2x1*GD1x2 + CKM2x2*GD2x2 + CKM2x3*GD3x2',
                  texname = '\\text{I4a22}')

I4a23 = Parameter(name = 'I4a23',
                  nature = 'internal',
                  type = 'complex',
                  value = 'CKM2x1*GD1x3 + CKM2x2*GD2x3 + CKM2x3*GD3x3',
                  texname = '\\text{I4a23}')

I4a31 = Parameter(name = 'I4a31',
                  nature = 'internal',
                  type = 'complex',
                  value = 'CKM3x1*GD1x1 + CKM3x2*GD2x1 + CKM3x3*GD3x1',
                  texname = '\\text{I4a31}')

I4a32 = Parameter(name = 'I4a32',
                  nature = 'internal',
                  type = 'complex',
                  value = 'CKM3x1*GD1x2 + CKM3x2*GD2x2 + CKM3x3*GD3x2',
                  texname = '\\text{I4a32}')

I4a33 = Parameter(name = 'I4a33',
                  nature = 'internal',
                  type = 'complex',
                  value = 'CKM3x1*GD1x3 + CKM3x2*GD2x3 + CKM3x3*GD3x3',
                  texname = '\\text{I4a33}')

I5a31 = Parameter(name = 'I5a31',
                  nature = 'internal',
                  type = 'complex',
                  value = 'yb*complexconjugate(CKM1x3)',
                  texname = '\\text{I5a31}')

I5a32 = Parameter(name = 'I5a32',
                  nature = 'internal',
                  type = 'complex',
                  value = 'yb*complexconjugate(CKM2x3)',
                  texname = '\\text{I5a32}')

I5a33 = Parameter(name = 'I5a33',
                  nature = 'internal',
                  type = 'complex',
                  value = 'yb*complexconjugate(CKM3x3)',
                  texname = '\\text{I5a33}')

I6a13 = Parameter(name = 'I6a13',
                  nature = 'internal',
                  type = 'complex',
                  value = 'yt*complexconjugate(CKM3x1)',
                  texname = '\\text{I6a13}')

I6a23 = Parameter(name = 'I6a23',
                  nature = 'internal',
                  type = 'complex',
                  value = 'yt*complexconjugate(CKM3x2)',
                  texname = '\\text{I6a23}')

I6a33 = Parameter(name = 'I6a33',
                  nature = 'internal',
                  type = 'complex',
                  value = 'yt*complexconjugate(CKM3x3)',
                  texname = '\\text{I6a33}')

I7a31 = Parameter(name = 'I7a31',
                  nature = 'internal',
                  type = 'complex',
                  value = 'CKM3x1*yt',
                  texname = '\\text{I7a31}')

I7a32 = Parameter(name = 'I7a32',
                  nature = 'internal',
                  type = 'complex',
                  value = 'CKM3x2*yt',
                  texname = '\\text{I7a32}')

I7a33 = Parameter(name = 'I7a33',
                  nature = 'internal',
                  type = 'complex',
                  value = 'CKM3x3*yt',
                  texname = '\\text{I7a33}')

I8a13 = Parameter(name = 'I8a13',
                  nature = 'internal',
                  type = 'complex',
                  value = 'CKM1x3*yb',
                  texname = '\\text{I8a13}')

I8a23 = Parameter(name = 'I8a23',
                  nature = 'internal',
                  type = 'complex',
                  value = 'CKM2x3*yb',
                  texname = '\\text{I8a23}')

I8a33 = Parameter(name = 'I8a33',
                  nature = 'internal',
                  type = 'complex',
                  value = 'CKM3x3*yb',
                  texname = '\\text{I8a33}')

