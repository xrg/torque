#include "license_pbs.h" /* See here for the software license */
#ifdef _AIX
#include <stdio.h>
#include <arpa/aixrcmds.h>
#endif

#include <pbs_config.h>   /* the master config generated by configure */

#include "portability.h"
#include "pbs_error.h"


/*
 * site_allow_u - site allow user access
 *
 * This routine determines if a user is privileged to access the batch
 * system on this host.
 *
 * It's implementation is "left as an exercise for the reader."
 *
 * Arguments: user - the user's name making the request
 *   host - host from which the user is making the request
 *
 * Returns: zero - if user is acceptable
 *   non-zero error number (PBSE_PERM) if not
 */

int
site_allow_u(char *user, char *host)
  {
  return 0;
  }
