# A Python API for the Full-Metadata Format

The Full-Metadata Format (FMF) is described in
[http://arxiv.org/abs/0904.1299](http://arxiv.org/abs/0904.1299). This
repository contains the description and implementation of a python API
for the FMF.

## License

Copyright (c) 2014, Rectorate of the University of Freiburg
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

* Redistributions of source code must retain the above copyright
  notice, this list of conditions and the following disclaimer.
* Redistributions in binary form must reproduce the above copyright
  notice, this list of conditions and the following disclaimer in the
  documentation and/or other materials provided with the distribution.
* Neither the name of the Freiburg Materials Research Center,
  University of Freiburg nor the names of its contributors may be used to
  endorse or promote products derived from this software without specific
  prior written permission.


THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS
IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED
TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A
PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER
OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

## Contents

* ./README.md             -- this file
* ./api.plantuml.txt      -- plantuml diagram source describing the API
* ./acceptance_tests/     -- acceptance tests / use case tests for the API
* ./streamlib/            -- the streamlib python package
* ./pyfmflib/
    * pyfmflib.cl1/       -- the pyfmflib.cl1 python package

## Acceptance tests

The acceptance tests are based on py.test. After installing
`pyfmflib.cl1` (requires `streamlib`), run them with

```
py.test acceptance_tests/
```

from the root of this repository. The API of `streamlib` and
`pyfmflib.cl1` is implicitly defined through the acceptance
tests. `api.plantuml.txt` makes these definitions explicit and is
extracted from the acceptance tests.

### Status

The compliance level 1 and streamlib API has converged but is still
open for minor changes that might become necessary during the
implementation.

## The streamlib package

The streamlib package is the only non-builtin dependency of
pyfmflib.cl1. It offers an abstract API for sending and translating
packets between sources and destinations.

### Status

The basic functionality has been implemented, yet unit tests are still
sparse.

## The pyfmflib.cl1 package

`pyfmflib` is a python namespace package. `pyfmflib.cl1` is the python package
that implements the compliance level 1 API.

### Status

The skeleton defined by the acceptance tests is finished. The
functionality and according unit tests are still missing.
